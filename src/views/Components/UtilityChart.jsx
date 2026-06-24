import { Bar } from "react-chartjs-2";

export default function UtilityChart({ weights }) {
  const data = {
    labels: ["Skin Match", "Acne Match", "Price Match"],
    datasets: [
      {
        label: "Weight Value",
        data: [weights.skin, weights.acne, weights.price],
        backgroundColor: ["#6C63FF", "#FF6584", "#44C5E5"]
      }
    ]
  };

  return (
    <div style={{ width: "100%", marginBottom: "20px" }}>
      <h3>User Utility Weights</h3>
      <Bar data={data} />
    </div>
  );
}
