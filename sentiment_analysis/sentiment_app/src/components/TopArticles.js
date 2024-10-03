import React from "react";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

export default function TopArticles(props) {
  return (
    <Box position="absolute" left="27.5%" width="35%" height="100%">
      <Grid container spacing={2} margin="auto" direction="column">
        <Grid item margin="auto">
          <Typography variant="subtitle2">
            {props.top_articles_pos[0].title}
          </Typography>
        </Grid>
        <Grid item margin="auto">
          <Typography variant="subtitle2">
            {props.top_articles_pos[1].title}
          </Typography>
        </Grid>
        <Grid item margin="auto">
          <Typography variant="subtitle2">
            {props.top_articles_pos[2].title}
          </Typography>
        </Grid>
        <Grid item margin="auto">
          <Typography variant="subtitle2">
            {props.top_articles_pos[3].title}
          </Typography>
        </Grid>
      </Grid>
      <Grid container spacing={2} margin="auto" direction="column">
        <Grid item margin="auto">
          <Typography variant="subtitle2">
            {props.top_articles_neg[0].title}
          </Typography>
        </Grid>
        <Grid item margin="auto">
          <Typography variant="subtitle2">
            {props.top_articles_neg[1].title}
          </Typography>
        </Grid>
        <Grid item margin="auto">
          <Typography variant="subtitle2">
            {props.top_articles_neg[2].title}
          </Typography>
        </Grid>
        <Grid item margin="auto">
          <Typography variant="subtitle2">
            {props.top_articles_neg[3].title}
          </Typography>
        </Grid>
      </Grid>
    </Box>
  );
}
