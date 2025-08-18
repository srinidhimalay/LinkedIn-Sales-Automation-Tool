//const API = "http://localhost:8000";
const API = "http://127.0.0.1:8000";

const createCampaign = async (data) => {
  try {
    const res = await fetch(`${API}/campaigns/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    return { error: err.message || "Failed to fetch" };
  }
};

export default { createCampaign };
