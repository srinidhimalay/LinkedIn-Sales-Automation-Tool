import React from "react";
import CampaignForm from "./components/CampaignForm";

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, errorInfo) {
    // You can log errorInfo here if needed
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ color: "red" }}>
          Error: {this.state.error && this.state.error.toString()}
        </div>
      );
    }
    return this.props.children;
  }
}

function App() {
  const [campaignId, setCampaignId] = React.useState(null);
  return (
    <ErrorBoundary>
      <div>
        <h1>LinkedIn Sales Automation Tool</h1>
        <div style={{ color: "green" }}>App loaded successfully</div>
        <CampaignForm onCreated={setCampaignId} />
      </div>
    </ErrorBoundary>
  );
}

export default App;
