import React from "react";

function ResultDisplay({ data }) {
  if (!data || typeof data !== "object") return null;

  const formatCurrency = (value) =>
    isNaN(value) ? "$0" : `$${parseFloat(value).toFixed(2)}`;

  return (
    <div className="result-container" style={{ background: "#e6ffe6", padding: "20px", marginTop: "20px" }}>
      <h2>Claim Result (#{data.claim_id ?? "-"})</h2>
      <p><strong>Status:</strong> {data.status ?? "-"}</p>
      <p><strong>Assessment:</strong> {data.assessment_confidence ?? "-"}</p>
      <p><strong>Monthly Rent:</strong> {formatCurrency(data.monthly_rent)}</p>
      <p><strong>Human Claimed:</strong> {formatCurrency(data.human_claimed_total)}</p>
      <p><strong>AI Approved:</strong> {formatCurrency(data.ai_approved_total)}</p>
      <p><strong>Final Payout:</strong> {formatCurrency(data.final_payout)}</p>
      <p><strong>Missing Documents:</strong> 
        {(Array.isArray(data.missing_docs) && data.missing_docs.length > 0)
          ? data.missing_docs.join(", ")
          : "None"}
      </p>
    </div>
  );
}

export default ResultDisplay;
