// src/controllers/actions.js

export const UploadImage = (imageSrc, navigate) => {
  fetch("/upload", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ file: imageSrc }),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        console.log("Please add a photograph");
      } else {
        console.log("Upload successful", data);
        navigate("/form", { state: { data } });
      }
    })
    .catch((err) => console.log(err.message));
};

export const putForm = (payload, navigate) => {
  console.log("Sending payload to backend:", payload);
  fetch("/recommend", {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        console.log("Error from backend:", data.error);
      } else {
        navigate("/recs", { state: { data } });
        console.log("Recommendations received:", data);
      }
    })
    .catch((err) => {
      console.log("Fetch error:", err);
    });
};
