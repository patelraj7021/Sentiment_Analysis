import React, { useState } from "react";
import Summary from "./Summary";
import SearchBar from "./SearchBar";
import TopArticles from "./TopArticles";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";
import { Button, TextField } from "@mui/material";

export default function App() {
  const [ticker, setTicker] = useState("NVDA");
  const [overall_rating, setOverallRating] = useState(50);
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
    const analyze_request_options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticker: ticker,
      }),
    };
    const pos_top_articles_options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticker: ticker,
        sort_order: "-overall_rating",
      }),
    };
    const neg_top_articles_options = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticker: ticker,
        sort_order: "overall_rating",
      }),
    };

    // chain fetch calls to update UI
    fetch("/sentiment-app/analyze-request", analyze_request_options)
      .then((response) => response.json())
      .then((data) => setOverallRating(data.overall_rating))
      .then(() => {
        // get articles with highest ratings in past 4 days
        return fetch("/sentiment-app/top-articles", pos_top_articles_options);
      })
      .then((response) => response.json())
      .then((data) => setTopArticlesPos(data))
      .then(() => {
        // get articles with lowest ratings in past 4 days
        return fetch("/sentiment-app/top-articles", neg_top_articles_options);
      })
      .then((response) => response.json())
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
        <Summary overall_rating={overall_rating} />
        <TopArticles
          top_articles_pos={top_articles_pos}
          top_articles_neg={top_articles_neg}
        />
      </Grid>
    </Grid>
  );
}
