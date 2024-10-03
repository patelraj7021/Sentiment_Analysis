import * as React from "react";
import { ScatterChart } from "@mui/x-charts/ScatterChart";
import { Box } from "@mui/material";

export default function Historical(props) {
  return (
    <Box position="absolute" width="30%" left="67.5%" height="100%">
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
      ></ScatterChart>
    </Box>
  );
}
