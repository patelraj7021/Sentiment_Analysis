import React, { useEffect, useState } from "react";
import Summary from "./Summary";
import SearchBar from "./SearchBar";
import TopArticles from "./TopArticles";
import Grid from "@mui/material/Grid2";
import Box from "@mui/material/Box";
import Historical from "./Historical";

export default function App() {
  const [ticker, setTicker] = useState("NVDA");
  const [circle_ratings, setCircleRatings] = useState([50, 50, 50]);
  const [loading, setLoading] = useState(false);
  const [top_articles_pos, setTopArticlesPos] = useState([
    { title: "-" },
    { title: "-" },
    { title: "-" },
    { title: "-" },
  ]);
  const [top_articles_neg, setTopArticlesNeg] = useState([
    { title: "-" },
    { title: "-" },
    { title: "-" },
    { title: "-" },
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
    // chain fetch calls to update UI
    fetch("/sentiment-app/") // empty call just for making button loading change work
      .then(() => {
        setLoading(true);
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

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box position="absolute" top="20%" width="100%">
        <SearchBar
          ticker={ticker}
          onChange={handleTickerChange}
          onClick={handleAnalyzePress}
          loading={loading}
        />
      </Box>
      <Box position="absolute" top="25%" width="100%" height="40%">
        <Summary circle_ratings={circle_ratings} />
        <TopArticles
          top_articles_pos={top_articles_pos}
          top_articles_neg={top_articles_neg}
        />
        <Historical historical_data={historical_data}></Historical>
      </Box>
      {/* <Grid container spacing={2} direction="column">
        <Grid item>
          <SearchBar
            ticker={ticker}
            onChange={handleTickerChange}
            onClick={handleAnalyzePress}
            loading={loading}
          />
        </Grid>
        <Grid item>
          <Grid container spacing={2}>
            <Summary circle_ratings={circle_ratings} />
            <TopArticles
              top_articles_pos={top_articles_pos}
              top_articles_neg={top_articles_neg}
            />
          </Grid>
        </Grid>
      </Grid> */}
    </Box>
  );
}
