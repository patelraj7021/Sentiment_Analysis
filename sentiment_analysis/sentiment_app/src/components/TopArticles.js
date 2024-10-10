import React from "react";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { CircularProgress } from "@mui/material";
import { green, red, grey } from "@mui/material/colors";
import Stack from "@mui/material";
import LaunchIcon from "@mui/icons-material/Launch";
import { IconButton } from "@mui/material";

export default function TopArticles(props) {
  const article_title_text_variant = "subtitle2";
  const section_header_variant = "h6";
  const article_rating_variant = "h6";

  const set_rating_color = (rating) => {
    if (rating <= 40) {
      return red[700];
    } else if (rating >= 60) {
      return green[700];
    } else {
      return grey[700];
    }
  };

  const generate_layout = (article_entry) => {
    return (
      <Grid item width="100%">
        <Grid
          container
          spacing={1}
          columns={11}
          sx={{ justifyContent: "center", alignItems: "center" }}
        >
          <Grid
            item
            size={1}
            sx={{ textAlign: "center", textJustify: "center" }}
          >
            <Box
              position="relative"
              width={35}
              height={35}
              sx={{
                bgcolor: set_rating_color(article_entry.overall_rating),
                borderRadius: "10%",
              }}
            >
              <Typography variant={article_rating_variant} color="white">
                {article_entry.overall_rating}
              </Typography>
            </Box>
          </Grid>
          <Grid item size={9}>
            <Typography
              noWrap={true}
              variant={article_title_text_variant}
              color="black"
            >
              {article_entry.title}
            </Typography>
          </Grid>
          <Grid item size={1}>
            <IconButton href={article_entry.link}>
              <LaunchIcon color="primary"></LaunchIcon>
            </IconButton>
          </Grid>
        </Grid>
      </Grid>
    );
  };

  return (
    <Grid item size={4}>
      <Grid container spacing={1} direction="column">
        <Grid item>
          <Typography variant={section_header_variant}>
            Optimistic Articles
          </Typography>
        </Grid>
        {generate_layout(props.top_articles_pos[0])}
        {generate_layout(props.top_articles_pos[1])}
        {generate_layout(props.top_articles_pos[2])}
        {generate_layout(props.top_articles_pos[3])}
        <Grid item>
          <Typography variant={section_header_variant}>
            Critical Articles
          </Typography>
        </Grid>
        {generate_layout(props.top_articles_neg[0])}
        {generate_layout(props.top_articles_neg[1])}
        {generate_layout(props.top_articles_neg[2])}
        {generate_layout(props.top_articles_neg[3])}
      </Grid>
    </Grid>
  );
}
