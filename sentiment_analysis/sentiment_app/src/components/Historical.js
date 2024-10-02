import * as React from "react";
import { ScatterChart } from "@mui/x-charts/ScatterChart";
import { Box } from "@mui/material";

export default function Historical(props) {
  return (
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
      height={400}
      width={400}
      xAxis={[{ scaleType: "time" }]}
    ></ScatterChart>
  );
}
