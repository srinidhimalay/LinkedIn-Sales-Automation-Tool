import React, { useState } from "react";
import api from "../api/api";
import { Box, Button, TextField, Typography, Paper } from "@mui/material";

const initialState = {
  product_service: "",
  description: "",
  target_industry: "",
  ideal_job_roles: "",
  company_size: "",
  region: "",
  outreach_goal: "",
  brand_voice: "",
  triggers: "",
};

export default function CampaignForm({ onCreated }) {
  const [form, setForm] = useState(initialState);
  const [error, setError] = useState("");
  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    const payload = {
      ...form,
      ideal_job_roles: form.ideal_job_roles.split(","),
      triggers: form.triggers.split(","),
    };
    const res = await api.createCampaign(payload);
    if (res.error) {
      setError(res.error);
    } else if (res.campaign) {
      onCreated(res.campaign.id);
    }
  };
  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 500, margin: "2rem auto" }}>
      <Typography variant="h5" gutterBottom>
        Create New Campaign
      </Typography>
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          Error: {error}
        </Typography>
      )}
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2,
        }}
      >
        <TextField
          name="product_service"
          label="Product/Service"
          onChange={handleChange}
          required
        />
        <TextField
          name="description"
          label="Description"
          onChange={handleChange}
          required
        />
        <TextField
          name="target_industry"
          label="Target Industry"
          onChange={handleChange}
          required
        />
        <TextField
          name="ideal_job_roles"
          label="Ideal Job Roles (comma separated)"
          onChange={handleChange}
          required
        />
        <TextField
          name="company_size"
          label="Company Size"
          onChange={handleChange}
          required
        />
        <TextField
          name="region"
          label="Region/Location"
          onChange={handleChange}
          required
        />
        <TextField
          name="outreach_goal"
          label="Outreach Goal"
          onChange={handleChange}
          required
        />
        <TextField
          name="brand_voice"
          label="Brand Voice"
          onChange={handleChange}
          required
        />
        <TextField
          name="triggers"
          label="Optional Triggers (comma separated)"
          onChange={handleChange}
        />
        <Button
          type="submit"
          variant="contained"
          color="primary"
          sx={{ mt: 2 }}
        >
          Create Campaign
        </Button>
      </Box>
    </Paper>
  );
}
