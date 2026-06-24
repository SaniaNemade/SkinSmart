import React, { useRef, useCallback, useState, useEffect } from "react";
import Webcam from "react-webcam";
import * as faceapi from "face-api.js";
import { UploadImage } from "../../controllers/actions";
import { useNavigate } from "react-router-dom";

// MUI
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";

const aspectRatio = 4 / 3;
const thresholdPercentFace = 0.3;
const thresholdFaceScore = 0.7;

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } = window;
  return { width, height };
}

function useWindowDimensions() {
  const [windowDimensions, setWindowDimensions] = useState(getWindowDimensions());
  useEffect(() => {
    const handleResize = () => setWindowDimensions(getWindowDimensions());
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  return windowDimensions;
}

const WebcamCapture = () => {
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  const { width: windowWidth, height: windowHeight } = useWindowDimensions();

  let camHeight = windowHeight * 0.6; // use 60% of height
  let camWidth = (camHeight / aspectRatio);

  const videoConstraints = {
    width: camWidth,
    height: camHeight,
    facingMode: "user",
  };

  const [initialising, setInitialising] = useState(false);
  const [faceOK, setFaceOK] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);

  // Load face-api.js models
  useEffect(() => {
    const loadModels = async () => {
      const MODEL_URI = process.env.PUBLIC_URL + "/models";
      setInitialising(true);
      await Promise.all([faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URI)]);
      setInitialising(false);
    };
    loadModels();
  }, []);

  // Face detection loop
  useEffect(() => {
    if (initialising || !webcamRef.current) return;

    const intervalId = setInterval(async () => {
      if (!webcamRef.current) return;

      const detections = await faceapi.detectAllFaces(
        webcamRef.current.video,
        new faceapi.TinyFaceDetectorOptions()
      );

      if (detections.length > 1) setFaceOK("Multiple faces detected");
      else if (detections[0]) {
        const boxArea =
          Math.round(detections[0].box.height) *
          Math.round(detections[0].box.width);
        const ImageArea = detections[0].imageWidth * detections[0].imageHeight;
        const percentFace = boxArea / ImageArea;

        if (percentFace < thresholdPercentFace) setFaceOK("Come closer");
        else if (detections[0].score < thresholdFaceScore)
          setFaceOK("Blurry or Not enough lighting");
        else setFaceOK("OK");
      } else setFaceOK("No face detected");
    }, 500);

    return () => clearInterval(intervalId);
  }, [initialising, webcamRef]);

  // Capture photo
  const capture = useCallback(() => {
    if (!webcamRef.current) return;
    const img = webcamRef.current.getScreenshot();
    console.log("Captured Image:", img);
    setImageSrc(img);
    if (img) UploadImage(img, navigate);
  }, [webcamRef, navigate]);

  return (
    <Grid
      container
      direction="column"
      justifyContent="center"
      alignItems="center"
      style={{ minHeight: "100vh", padding: "1rem" }}
    >
      <Grid item>
        <Typography variant="h5" textAlign="center" gutterBottom>
          {initialising ? "Initialising..." : faceOK || "Position your face"}
        </Typography>
      </Grid>

      <Grid item style={{ marginTop: "1rem", marginBottom: "2rem" }}>
        <Webcam
          audio={false}
          height={videoConstraints.height}
          width={videoConstraints.width}
          ref={webcamRef}
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
          style={{ borderRadius: "10px", border: "2px solid #ccc" }}
        />
      </Grid>

      <Grid item style={{ width: "100%", maxWidth: "400px" }}>
        <Button
          onClick={capture}
          variant="contained"
          fullWidth
          disabled={initialising || faceOK !== "OK"}
        >
          Capture photo
        </Button>
      </Grid>
    </Grid>
  );
};

export default WebcamCapture;
