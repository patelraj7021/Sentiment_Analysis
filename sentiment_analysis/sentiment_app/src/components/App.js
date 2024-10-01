import React, { useState } from "react";
import Summary from "./Summary";
import SearchBar from "./SearchBar";
import TopArticles from "./TopArticles";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";
import { Button, TextField } from "@mui/material";

export default function App() {
  const [ticker, setTicker] = useState("NVDA");
  const [circle_ratings, setCircleRatings] = useState([50, 50, 50]);
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
    fetch("/sentiment-app/analyze-request", analyze_request_options)
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
      .then((data) => setTopArticlesNeg(data));
  };

  return (
    <Grid container spacing={2} margin="auto" direction="column">
      <SearchBar
        ticker={ticker}
        onChange={handleTickerChange}
        onClick={handleAnalyzePress}
      />
      <Grid container spacing={2}>
        <Summary circle_ratings={circle_ratings} />
        <TopArticles
          top_articles_pos={top_articles_pos}
          top_articles_neg={top_articles_neg}
        />
      </Grid>
    </Grid>
  );
}
