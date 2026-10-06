import os

import streamlit as st

from backend.scrapers.instagram_scraper import scrape_instagram
from backend.analytics.analytics import generate_analytics
from backend.visualization.charts import generate_charts
from backend.llm.llm import generate_recommendations


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


instagram_url = st.text_input(
    "Enter Instagram Profile URL",
    placeholder="https://www.instagram.com/username/"
)


if st.button("Analyze Profile"):

    if not instagram_url:

        st.warning(
            "Please enter an Instagram profile URL."
        )

    else:

        # -----------------------------------
        # Instagram Scraping
        # -----------------------------------

        with st.spinner(
            "Scraping Instagram profile..."
        ):

            profile = scrape_instagram(
                instagram_url
            )


        if profile is None:

            st.error(
                "Instagram profile could not be collected."
            )

        else:

            st.success(
                "Instagram profile collected successfully!"
            )


            # -----------------------------------
            # Profile Details
            # -----------------------------------

            st.subheader("Profile Details")


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "Username",
                    profile.get(
                        "username",
                        "N/A"
                    )
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
                "Yes" if verified else "No"
            )


            # -----------------------------------
            # Analytics
            # -----------------------------------

            st.divider()

            st.subheader("📈 Follower Growth")


            with st.spinner(
                "Calculating Instagram analytics..."
            ):

                report = generate_analytics()


            if report is None:

                st.error(
                    "Analytics generation failed."
                )

            else:

                st.success(
                    "Analytics generated successfully!"
                )


                # -----------------------------------
                # Follower Growth Details
                # -----------------------------------

                growth = report.get(
                    "growth",
                    {}
                )


                col1, col2, col3, col4 = st.columns(4)


                with col1:

                    st.metric(
                        "Start Followers",
                        f"{growth.get('start_followers', 0):,}"
                    )


                with col2:

                    st.metric(
                        "Current Followers",
                        f"{growth.get('end_followers', 0):,}"
                    )


                with col3:

                    growth_value = growth.get(
                        "growth",
                        0
                    )

                    st.metric(
                        "Growth",
                        f"{growth_value:+,}"
                    )


                with col4:

                    growth_percentage = growth.get(
                        "growth_percentage",
                        0
                    )

                    st.metric(
                        "Growth %",
                        f"{growth_percentage:+.2f}%"
                    )


                direction = growth.get(
                    "direction",
                    "unknown"
                )


                if direction == "increase":

                    st.success(
                        "Follower growth increased 📈"
                    )

                elif direction == "decrease":

                    st.error(
                        "Follower growth decreased 📉"
                    )

                else:

                    st.info(
                        "No follower growth recorded."
                    )


                # -----------------------------------
                # Generate Charts
                # -----------------------------------

                st.divider()

                st.subheader(
                    "📊 Instagram Analytics Charts"
                )


                with st.spinner(
                    "Generating analytics charts..."
                ):

                    generate_charts()


                # -----------------------------------
                # Display Charts
                # -----------------------------------

                col1, col2 = st.columns(2)


                # -----------------------------------
                # Left Column
                # -----------------------------------

                with col1:

                    content_chart = (
                        "backend/visualization/"
                        "content_distribution.png"
                    )


                    if os.path.exists(
                        content_chart
                    ):

                        st.subheader(
                            "Content Distribution"
                        )

                        st.image(
                            content_chart,
                            use_container_width=True
                        )


                    posting_chart = (
                        "backend/visualization/"
                        "posting_time_performance.png"
                    )


                    if os.path.exists(
                        posting_chart
                    ):

                        st.subheader(
                            "Posting Time Performance"
                        )

                        st.image(
                            posting_chart,
                            use_container_width=True
                        )


                # -----------------------------------
                # Right Column
                # -----------------------------------

                with col2:

                    likes_chart = (
                        "backend/visualization/"
                        "average_likes_content_type.png"
                    )


                    if os.path.exists(
                        likes_chart
                    ):

                        st.subheader(
                            "Average Likes by Content Type"
                        )

                        st.image(
                            likes_chart,
                            use_container_width=True
                        )


                    top_posts_chart = (
                        "backend/visualization/"
                        "top_3_posts.png"
                    )


                    if os.path.exists(
                        top_posts_chart
                    ):

                        st.subheader(
                            "Top 3 Performing Posts"
                        )

                        st.image(
                            top_posts_chart,
                            use_container_width=True
                        )
                # -----------------------------------
                # AI Growth Recommendations
                # -----------------------------------

                st.divider()

                st.subheader(
                    "🤖 AI Growth Recommendations"
                )

                with st.spinner(
                    "Generating AI growth recommendations..."
                ):

                    try:

                        llm_response = generate_recommendations()

                        st.success(
                            "AI recommendations generated successfully!"
                        )

                        st.markdown(
                            llm_response
                        )

                    except Exception as error:

                        st.error(
                            f"AI recommendation generation failed: {error}"
                        )