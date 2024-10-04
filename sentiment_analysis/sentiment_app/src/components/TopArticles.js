import React from "react";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

export default function TopArticles(props) {
  const article_title_text_variant = "subtitle2";
  const section_header_variant = "h6";
  return (
    <Grid item size={4}>
      <Grid container spacing={2} direction="column">
        <Grid item>
          <Typography variant={section_header_variant}>
            Optimistic Articles
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant={article_title_text_variant}>
            {props.top_articles_pos[0].title}
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant={article_title_text_variant}>
            {props.top_articles_pos[1].title}
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant={article_title_text_variant}>
            {props.top_articles_pos[2].title}
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant={article_title_text_variant}>
            {props.top_articles_pos[3].title}
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant={section_header_variant}>
            Critical Articles
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant={article_title_text_variant}>
            {props.top_articles_neg[0].title}
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant={article_title_text_variant}>
            {props.top_articles_neg[1].title}
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant={article_title_text_variant}>
            {props.top_articles_neg[2].title}
          </Typography>
        </Grid>
        <Grid item>
          <Typography variant={article_title_text_variant}>
            {props.top_articles_neg[3].title}
          </Typography>
        </Grid>
      </Grid>
    </Grid>
  );
}
