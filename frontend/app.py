import json
import os
from datetime import datetime

import streamlit as st

from backend.analytics.analytics import generate_analytics
from backend.llm.llm import generate_recommendations
from backend.scrapers.instagram_scraper import scrape_instagram
from backend.visualization.charts import generate_charts


st.set_page_config(
    page_title="Instagram AI Growth Report",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Instagram AI Growth Report")

st.write(
    "Analyze Instagram profile growth, post performance, "
    "and get AI-powered growth recommendations."
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "profile" not in st.session_state:
    st.session_state.profile = None

if "report" not in st.session_state:
    st.session_state.report = None

if "analyzed_url" not in st.session_state:
    st.session_state.analyzed_url = ""

if "llm_recommendations" not in st.session_state:
    st.session_state.llm_recommendations = None

if "filter_months" not in st.session_state:
    st.session_state.filter_months = False

if "start_month" not in st.session_state:
    st.session_state.start_month = None

if "end_month" not in st.session_state:
    st.session_state.end_month = None


# ---------------------------------------------------------
# INSTAGRAM URL INPUT
# ---------------------------------------------------------

instagram_url = st.text_input(
    "Enter Instagram Profile URL",
    placeholder="https://www.instagram.com/username/"
)


# ---------------------------------------------------------
# ANALYZE PROFILE
# ---------------------------------------------------------

if st.button("Analyze Profile", type="primary"):

    if not instagram_url.strip():
        st.warning("Please enter an Instagram profile URL.")

    else:

        # Reset previous analysis before starting a new one
        st.session_state.analysis_done = False
        st.session_state.profile = None
        st.session_state.report = None
        st.session_state.llm_recommendations = None

        # Reset follower filters for the new profile
        st.session_state.filter_months = False
        st.session_state.start_month = None
        st.session_state.end_month = None

        # -------------------------------------------------
        # SCRAPING
        # -------------------------------------------------

        with st.spinner("Scraping Instagram profile..."):

            try:
                profile = scrape_instagram(instagram_url.strip())

            except Exception as error:
                profile = None
                st.error(
                    f"Instagram scraping failed: {error}"
                )

        if profile is None:

            st.error(
                "Instagram profile could not be collected."
            )

        else:

            # -------------------------------------------------
            # ANALYTICS
            # -------------------------------------------------

            with st.spinner("Calculating Instagram analytics..."):

                try:
                    report = generate_analytics()

                except Exception as error:
                    report = None
                    st.error(
                        f"Analytics generation failed: {error}"
                    )

            if report is None:

                st.error(
                    "Analytics report could not be generated."
                )

            else:

                # -------------------------------------------------
                # SAVE CURRENT PROFILE REPORT
                # -------------------------------------------------

                st.session_state.profile = profile
                st.session_state.report = report
                st.session_state.analyzed_url = instagram_url.strip()

                # -------------------------------------------------
                # GEMINI RECOMMENDATIONS
                # -------------------------------------------------

                try:

                    with st.spinner(
                        "Generating AI growth recommendations..."
                    ):

                        llm_recommendations = (
                            generate_recommendations()
                        )

                    st.session_state.llm_recommendations = (
                        llm_recommendations
                    )

                except Exception as error:

                    st.session_state.llm_recommendations = None

                    st.warning(
                        f"AI recommendations could not be generated: {error}"
                    )

                # -------------------------------------------------
                # ANALYSIS COMPLETE
                # -------------------------------------------------

                st.session_state.analysis_done = True

                st.success(
                    "Instagram profile analyzed successfully!"
                )


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

if st.session_state.analysis_done:

    profile = st.session_state.profile
    report = st.session_state.report

    if profile is None or report is None:

        st.error(
            "Analysis data is unavailable. Please analyze the profile again."
        )

        st.stop()


    # ---------------------------------------------------------
    # CURRENT PROFILE
    # ---------------------------------------------------------

    current_username = profile.get(
        "username",
        "N/A"
    )

    st.success(
        f"Showing analysis for: {st.session_state.analyzed_url}"
    )


    # ---------------------------------------------------------
    # PROFILE DETAILS
    # ---------------------------------------------------------

    st.subheader("👤 Profile Details")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Username",
            current_username
        )

    with col2:

        followers = profile.get(
            "followersCount",
            0
        )

        st.metric(
            "Followers",
            f"{followers:,}"
        )

    with col3:

        following = profile.get(
            "followsCount"
        )

        if following is not None:

            st.metric(
                "Following",
                f"{following:,}"
            )

        else:

            st.metric(
                "Following",
                "N/A"
            )

    with col4:

        posts = profile.get(
            "postsCount",
            0
        )

        st.metric(
            "Posts",
            f"{posts:,}"
        )


    verified = profile.get(
        "verified",
        False
    )

    st.write(
        "Verified:",
        "Yes ✅" if verified else "No"
    )

    st.divider()


    # ---------------------------------------------------------
    # FOLLOWER GROWTH
    # ---------------------------------------------------------

    st.subheader("📈 Follower Growth")

    history_file = (
        "backend/data/profile_history.json"
    )

    if not os.path.exists(history_file):

        st.info(
            "Follower history is not available yet."
        )

    else:

        try:

            with open(
                history_file,
                "r",
                encoding="utf-8"
            ) as file:

                history = json.load(file)

        except Exception as error:

            st.error(
                f"Could not read follower history: {error}"
            )

            history = []


        # -----------------------------------------------------
        # FILTER HISTORY FOR CURRENT PROFILE ONLY
        # -----------------------------------------------------

        user_history = [
            item
            for item in history
            if item.get("username") == current_username
        ]


        # Sort current profile's history only
        user_history = sorted(
            user_history,
            key=lambda item: item.get(
                "date",
                ""
            )
        )


        # Remove invalid snapshots
        valid_history = [
            item
            for item in user_history
            if (
                item.get("date")
                and item.get("followers") is not None
            )
        ]


        # -----------------------------------------------------
        # TWO OR MORE SNAPSHOTS
        # -----------------------------------------------------

        if len(valid_history) >= 2:

            filter_months = st.checkbox(
                "Filter by months",
                key="filter_months"
            )


            # -------------------------------------------------
            # COMPLETE HISTORY
            # -------------------------------------------------

            if not filter_months:

                first = valid_history[0]
                last = valid_history[-1]

                start_followers = first["followers"]
                end_followers = last["followers"]

                growth = (
                    end_followers
                    - start_followers
                )

                if start_followers > 0:

                    growth_percentage = (
                        growth
                        / start_followers
                    ) * 100

                else:

                    growth_percentage = 0


                st.write(
                    f"Showing complete follower history: "
                    f"{first['date']} → {last['date']}"
                )


                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Start Followers",
                        f"{start_followers:,}"
                    )

                with col2:

                    st.metric(
                        "End Followers",
                        f"{end_followers:,}"
                    )

                with col3:

                    st.metric(
                        "Growth",
                        f"{growth:+,}"
                    )

                with col4:

                    st.metric(
                        "Growth %",
                        f"{growth_percentage:+.2f}%"
                    )


                if growth > 0:

                    st.success(
                        "Follower growth increased 📈"
                    )

                elif growth < 0:

                    st.error(
                        "Follower growth decreased 📉"
                    )

                else:

                    st.info(
                        "No follower growth was recorded."
                    )


            # -------------------------------------------------
            # MONTH FILTER
            # -------------------------------------------------

            else:

                try:

                    first_date = datetime.strptime(
                        valid_history[0]["date"],
                        "%Y-%m-%d"
                    )

                    last_date = datetime.strptime(
                        valid_history[-1]["date"],
                        "%Y-%m-%d"
                    )

                except ValueError:

                    st.error(
                        "Follower history contains an invalid date format."
                    )

                    first_date = None
                    last_date = None


                if first_date and last_date:

                    # -----------------------------------------
                    # CREATE ALL MONTHS BETWEEN FIRST/LAST DATE
                    # -----------------------------------------

                    available_months = []

                    current_year = first_date.year
                    current_month = first_date.month

                    while (
                        current_year < last_date.year
                        or (
                            current_year == last_date.year
                            and current_month <= last_date.month
                        )
                    ):

                        available_months.append(
                            f"{current_year:04d}-{current_month:02d}"
                        )

                        if current_month == 12:

                            current_month = 1
                            current_year += 1

                        else:

                            current_month += 1


                    # -----------------------------------------
                    # MONTH SELECTORS
                    # -----------------------------------------

                    col1, col2 = st.columns(2)

                    with col1:

                        start_month = st.selectbox(
                            "Start Month",
                            available_months,
                            index=0,
                            key="start_month"
                        )

                    with col2:

                        end_month = st.selectbox(
                            "End Month",
                            available_months,
                            index=len(available_months) - 1,
                            key="end_month"
                        )


                    # -----------------------------------------
                    # INVALID RANGE
                    # -----------------------------------------

                    if start_month > end_month:

                        st.warning(
                            "Please select a start month that "
                            "comes before the end month."
                        )


                    else:

                        # -------------------------------------
                        # FIND CURRENT PROFILE DATA
                        # -------------------------------------

                        start_data = [
                            item
                            for item in valid_history
                            if item["date"][:7] == start_month
                        ]

                        end_data = [
                            item
                            for item in valid_history
                            if item["date"][:7] == end_month
                        ]


                        # -------------------------------------
                        # START MONTH NOT AVAILABLE
                        # -------------------------------------

                        if not start_data:

                            st.warning(
                                f"Follower data is not available "
                                f"for {start_month}. Please select "
                                f"a month with stored follower history."
                            )


                        # -------------------------------------
                        # END MONTH NOT AVAILABLE
                        # -------------------------------------

                        elif not end_data:

                            st.warning(
                                f"Follower data is not available "
                                f"for {end_month}. Please select "
                                f"a month with stored follower history."
                            )


                        # -------------------------------------
                        # CALCULATE FILTERED GROWTH
                        # -------------------------------------

                        else:

                            start_snapshot = start_data[0]
                            end_snapshot = end_data[-1]

                            start_followers = (
                                start_snapshot["followers"]
                            )

                            end_followers = (
                                end_snapshot["followers"]
                            )

                            growth = (
                                end_followers
                                - start_followers
                            )

                            if start_followers > 0:

                                growth_percentage = (
                                    growth
                                    / start_followers
                                ) * 100

                            else:

                                growth_percentage = 0


                            st.write(
                                f"Showing follower growth from "
                                f"{start_snapshot['date']} to "
                                f"{end_snapshot['date']}"
                            )


                            col1, col2, col3, col4 = st.columns(4)

                            with col1:

                                st.metric(
                                    "Start Followers",
                                    f"{start_followers:,}"
                                )

                            with col2:

                                st.metric(
                                    "End Followers",
                                    f"{end_followers:,}"
                                )

                            with col3:

                                st.metric(
                                    "Growth",
                                    f"{growth:+,}"
                                )

                            with col4:

                                st.metric(
                                    "Growth %",
                                    f"{growth_percentage:+.2f}%"
                                )


                            if growth > 0:

                                st.success(
                                    f"Follower growth increased "
                                    f"from {start_month} to "
                                    f"{end_month} 📈"
                                )

                            elif growth < 0:

                                st.error(
                                    f"Follower growth decreased "
                                    f"from {start_month} to "
                                    f"{end_month} 📉"
                                )

                            else:

                                st.info(
                                    "Follower count remained unchanged."
                                )


        # -----------------------------------------------------
        # ONLY ONE SNAPSHOT
        # -----------------------------------------------------

        elif len(valid_history) == 1:

            snapshot = valid_history[0]

            st.info(
                f"Follower tracking started on "
                f"{snapshot['date']}. "
                "More snapshots are required to calculate growth."
            )


        # -----------------------------------------------------
        # NO SNAPSHOTS
        # -----------------------------------------------------

        else:

            st.info(
                "No follower history is available yet."
            )


    st.divider()


    # ---------------------------------------------------------
    # AI GROWTH RECOMMENDATIONS
    # ---------------------------------------------------------

    st.subheader(
        "🤖 AI Growth Recommendations"
    )

    llm_recommendations = (
        st.session_state.get(
            "llm_recommendations"
        )
    )


    if llm_recommendations:

        if isinstance(
            llm_recommendations,
            str
        ):

            st.markdown(
                llm_recommendations
            )


        elif isinstance(
            llm_recommendations,
            dict
        ):

            recommendation_text = (
                llm_recommendations.get(
                    "recommendations"
                )
                or llm_recommendations.get(
                    "response"
                )
                or llm_recommendations.get(
                    "text"
                )
            )


            if recommendation_text:

                st.markdown(
                    recommendation_text
                )

            else:

                st.json(
                    llm_recommendations
                )


        else:

            st.write(
                llm_recommendations
            )


    else:

        st.info(
            "AI growth recommendations are not available "
            "for this analysis."
        )


    st.divider()


    # ---------------------------------------------------------
    # CHARTS
    # ---------------------------------------------------------

    st.subheader(
        "📊 Instagram Analytics Charts"
    )


    # IMPORTANT:
    # Charts are generated directly from the CURRENT report.
    # No old PNG files are used.
    try:

        charts = generate_charts(
            report
        )

    except Exception as error:

        st.error(
            f"Charts could not be generated: {error}"
        )

        charts = {}


    col1, col2 = st.columns(2)


    # ---------------------------------------------------------
    # LEFT COLUMN
    # ---------------------------------------------------------

    with col1:

        if charts.get(
            "content_distribution"
        ) is not None:

            st.subheader(
                "Content Distribution"
            )

            st.pyplot(
                charts["content_distribution"],
                clear_figure=True
            )


        if charts.get(
            "posting_time"
        ) is not None:

            st.subheader(
                "Posting Time Performance"
            )

            st.pyplot(
                charts["posting_time"],
                clear_figure=True
            )


    # ---------------------------------------------------------
    # RIGHT COLUMN
    # ---------------------------------------------------------

    with col2:

        if charts.get(
            "average_likes"
        ) is not None:

            st.subheader(
                "Average Likes by Content Type"
            )

            st.pyplot(
                charts["average_likes"],
                clear_figure=True
            )


        if charts.get(
            "top_posts"
        ) is not None:

            st.subheader(
                "Top 3 Performing Posts"
            )

            st.pyplot(
                charts["top_posts"],
                clear_figure=True
            )