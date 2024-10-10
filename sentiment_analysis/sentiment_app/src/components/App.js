import React, { useEffect, useState } from "react";
import Summary from "./Summary";
import SearchBar from "./SearchBar";
import TopArticles from "./TopArticles";
import Grid from "@mui/material/Grid2";
import Box from "@mui/material/Box";
import Historical from "./Historical";
import { Container, Typography } from "@mui/material";
import { pink, yellow } from "@mui/material/colors";

export default function App() {
  const [ticker, setTicker] = useState("NVDA");
  const [circle_ratings, setCircleRatings] = useState([50, 50, 50]);
  const [loading, setLoading] = useState(false);
  const [top_articles_pos, setTopArticlesPos] = useState([
    { title: "-", overall_rating: 50, link: "/sentiment-app/" },
    { title: "-", overall_rating: 50, link: "/sentiment-app/" },
    { title: "-", overall_rating: 50, link: "/sentiment-app/" },
    { title: "-", overall_rating: 50, link: "/sentiment-app/" },
  ]);
  const [top_articles_neg, setTopArticlesNeg] = useState([
    { title: "-", overall_rating: 50, link: "/sentiment-app/" },
    { title: "-", overall_rating: 50, link: "/sentiment-app/" },
    { title: "-", overall_rating: 50, link: "/sentiment-app/" },
    { title: "-", overall_rating: 50, link: "/sentiment-app/" },
  ]);
  const [historical_data, setHistoricalData] = useState([]);

  const handleTickerChange = (e) => {
    setTicker(e.target.value);
  };

  const handleAnalyzePress = () => {
    // generate options for requests later
    // eaiser to wrap some in functions for repeat calls
    // with minor differences
    const analyze_request_options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticker: ticker,
      }),
    };

    const summary_circle_options = (date_delta) => {
      return {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker: ticker,
          date_delta: date_delta,
        }),
      };
    };

    const top_articles_options = (sort_order) => {
      return {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker: ticker,
          sort_order: sort_order,
        }),
      };
    };

    let new_summary_circle_values = new Array(3);
    // fetch existing data for quick update
    fetch("/sentiment-app/summary-circle", summary_circle_options(1))
      .then((response) => response.json())
      .then((data) => {
        setLoading(true);
        new_summary_circle_values[0] = data.overall_rating;
        // update past 3 days summary circle
        return fetch(
          "/sentiment-app/summary-circle",
          summary_circle_options(4)
        );
      })
      .then((response) => response.json())
      .then((data) => {
        new_summary_circle_values[1] = data.overall_rating;
        // update past 7 days summary circle
        return fetch(
          "/sentiment-app/summary-circle",
          summary_circle_options(8)
        );
      })
      .then((response) => response.json())
      .then((data) => {
        new_summary_circle_values[2] = data.overall_rating;
        // set state for Summary component
        setCircleRatings(new_summary_circle_values);
        // get articles with highest ratings in past 4 days
        return fetch(
          "/sentiment-app/top-articles",
          top_articles_options("-overall_rating")
        );
      })
      .then((response) => response.json())
      // set state for articles with highest ratings
      .then((data) => setTopArticlesPos(data))
      .then(() => {
        // get articles with lowest ratings in past 4 days
        return fetch(
          "/sentiment-app/top-articles",
          top_articles_options("overall_rating")
        );
      })
      .then((response) => response.json())
      // set state for articles with lowest ratings
      .then((data) => {
        setTopArticlesNeg(data);
      })
      .then(() => {
        // get historical summaries data for past 30 days
        return fetch("/sentiment-app/historical", analyze_request_options);
      })
      .then((response) => response.json())
      // set state for historical data
      .then((data) => {
        setHistoricalData(data);
      });

    // fetch articles and update again
    fetch("/sentiment-app/") // empty call just for making button loading change work
      .then(() => {
        return fetch("/sentiment-app/analyze-request", analyze_request_options);
      })
      .then(() => {
        // update today summary circle
        return fetch(
          "/sentiment-app/summary-circle",
          summary_circle_options(1)
        );
      })
      .then((response) => response.json())
      .then((data) => {
        new_summary_circle_values[0] = data.overall_rating;
        // update past 3 days summary circle
        return fetch(
          "/sentiment-app/summary-circle",
          summary_circle_options(4)
        );
      })
      .then((response) => response.json())
      .then((data) => {
        new_summary_circle_values[1] = data.overall_rating;
        // update past 7 days summary circle
        return fetch(
          "/sentiment-app/summary-circle",
          summary_circle_options(8)
        );
      })
      .then((response) => response.json())
      .then((data) => {
        new_summary_circle_values[2] = data.overall_rating;
        // set state for Summary component
        setCircleRatings(new_summary_circle_values);
        // get articles with highest ratings in past 4 days
        return fetch(
          "/sentiment-app/top-articles",
          top_articles_options("-overall_rating")
        );
      })
      .then((response) => response.json())
      // set state for articles with highest ratings
      .then((data) => setTopArticlesPos(data))
      .then(() => {
        // get articles with lowest ratings in past 4 days
        return fetch(
          "/sentiment-app/top-articles",
          top_articles_options("overall_rating")
        );
      })
      .then((response) => response.json())
      // set state for articles with lowest ratings
      .then((data) => {
        setTopArticlesNeg(data);
      })
      .then(() => {
        // get historical summaries data for past 30 days
        return fetch("/sentiment-app/historical", analyze_request_options);
      })
      .then((response) => response.json())
      // set state for historical data
      .then((data) => {
        setHistoricalData(data);
      })
      .then(() => {
        setLoading(false);
      });
  };

  const section_header_variant = "h5";

  return (
    <Box
      sx={{
        flexGrow: 1,
        background: "linear-gradient(to right bottom, #f48fb1, #fff59d)",
      }}
      height="100%"
      justifyContent="center"
      alignItems="center"
      display="flex"
    >
      <Box
        height={900}
        width={1440}
        justifyContent="center"
        alignItems="center"
      >
        <Box
          position="relative"
          height="96%"
          width="96%"
          top="2%"
          left="2%"
          sx={{ bgcolor: "white", borderRadius: "2.5%" }}
        >
          <Box position="relative" height="98%" width="98%" top="1%" left="1%">
            <Grid
              container
              spacing={3}
              sx={{ justifyContent: "center", alignItems: "center" }}
              direction="column"
            >
              <Grid item>
                <Typography variant="h4"> Stock Sentiment Analyzer </Typography>
              </Grid>
              <Grid
                container
                spacing={2}
                sx={{ justifyContent: "center", alignItems: "center" }}
              >
                <SearchBar
                  ticker={ticker}
                  onChange={handleTickerChange}
                  onClick={handleAnalyzePress}
                  loading={loading}
                />
              </Grid>
              <Grid
                container
                spacing={2}
                sx={{
                  justifyContent: "center",
                  alignItems: "center",
                  textAlign: "center",
                }}
                columns={12}
                width="100%"
              >
                <Grid item size={4}>
                  <Typography variant={section_header_variant}>
                    Sentiment Overviews
                  </Typography>
                </Grid>
                <Grid item size={4}>
                  <Typography variant={section_header_variant}>
                    Top Recent Articles
                  </Typography>
                </Grid>
                <Grid item size={4}>
                  <Typography variant={section_header_variant}>
                    Monthly Trend
                  </Typography>
                </Grid>
              </Grid>
              <Grid
                container
                spacing={2}
                sx={{ justifyContent: "center", alignItems: "flex-start" }}
                columns={12}
                width="100%"
              >
                <Summary circle_ratings={circle_ratings} />
                <TopArticles
                  top_articles_pos={top_articles_pos}
                  top_articles_neg={top_articles_neg}
                />
                <Historical historical_data={historical_data}></Historical>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Box>
    </Box>
  );
}
