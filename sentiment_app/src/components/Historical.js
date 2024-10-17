import * as React from "react";
import { ScatterChart } from "@mui/x-charts/ScatterChart";
import { Box } from "@mui/material";
import Grid from "@mui/material/Grid2";

export default function Historical(props) {
  return (
    <Grid item size={4}>
      <ScatterChart
        series={[
          {
            data: props.historical_data.map((v) => ({
              x: new Date(v.date),
              y: v.overall_rating,
              id: v.id,
            })),
          },
        ]}
        xAxis={[{ scaleType: "utc" }]}
        height={400}
      ></ScatterChart>
    </Grid>
  );
}
