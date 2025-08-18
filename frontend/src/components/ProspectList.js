import React from "react";
import { Box, Typography, Card, CardContent, Link, Grid } from "@mui/material";

export default function ProspectList({ prospects }) {
  if (!prospects.length) return <Typography>No prospects yet.</Typography>;
  return (
    <Box>
      <Typography variant="h6" sx={{ mb: 2 }}>
        Prospects
      </Typography>
      <Grid container spacing={2}>
        {prospects.map((p, i) => (
          <Grid item xs={12} md={6} key={i}>
            <Card variant="outlined">
              <CardContent>
                <Typography variant="subtitle1">
                  <b>{p.name}</b> ({p.title} @ {p.company})
                </Typography>
                <Link
                  href={p.profile_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View LinkedIn Profile
                </Link>
                {p.message && (
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    <i>{p.message}</i>
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
