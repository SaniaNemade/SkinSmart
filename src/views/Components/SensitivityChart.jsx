import { Line } from "react-chartjs-2";

export default function SensitivityChart({ sensitivity }) {
  const labels = ["Original", "Skin +10%", "Acne +10%", "Price +10%"];

  const data = {
    labels,
    datasets: [
      {
        label: "Rank 1 Category",
        data: [
          sensitivity.original_top[0],
          sensitivity.skin_plus_top[0],
          sensitivity.acne_plus_top[0],
          sensitivity.price_plus_top[0]
        ],
        borderColor: "#4CAF50",
        borderWidth: 2
      }
    ]
  };

  return (
    <div style={{ width: "100%", margin: "20px 0" }}>
      <h3>Sensitivity Analysis</h3>
      <p>Shows how Rank 1 category changes when weights change slightly</p>
      <Line data={data} />
    </div>
  );
}
