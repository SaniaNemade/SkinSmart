import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

// MUI
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import Checkbox from "@mui/material/Checkbox";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";

// controllers
import { putForm } from "../controllers/actions";

const skinToneValues = [1, 2, 3, 4, 5, 6];
const skinToneColors = [
  "rgb(249, 245, 236)",
  "rgb(250, 245, 234)",
  "rgb(240, 227, 171)",
  "rgb(206, 172, 104)",
  "rgb(105, 59, 41)",
  "rgb(33, 28, 40)",
];

const skinTypes = ["All", "Oily", "Normal", "Dry"];
const acnes = ["Low", "Moderate", "Severe"];
const otherConcerns = [
  "sensitive",
  "fine lines",
  "wrinkles",
  "redness",
  "pore",
  "pigmentation",
  "blackheads",
  "whiteheads",
  "blemishes",
  "dark circles",
  "eye bags",
  "dark spots",
];

const weightOptions = [1, 2, 3, 4, 5];

const Form = () => {
  const { state } = useLocation();
  let prefill = { tone: 5, type: "Oily", acne: "Moderate" };

  if (state !== null) prefill = state.data;

  const navigate = useNavigate();

  const [currType, setCurrType] = useState(prefill.type);
  const [currTone, setCurrTone] = useState(parseInt(prefill.tone));
  const [currAcne, setAcne] = useState(prefill.acne);

  const [features, setFeatures] = useState({
    normal: false,
    dry: false,
    oily: false,
    combination: false,
    acne: false,
    sensitive: false,
    "fine lines": false,
    wrinkles: false,
    redness: false,
    dull: false,
    pore: false,
    pigmentation: false,
    blackheads: false,
    whiteheads: false,
    blemishes: false,
    "dark circles": false,
    "eye bags": false,
    "dark spots": false,
  });

  // ⭐ NEW STATES FOR WEIGHTS
  const [weightSkinConcern, setWeightSkinConcern] = useState(3);
  const [weightAcneConcern, setWeightAcneConcern] = useState(3);
  const [weightPrice, setWeightPrice] = useState(3);

  const handleChange = (event) => {
    setFeatures({
      ...features,
      [event.target.name]: event.target.checked,
    });
  };

  const handleSubmit = () => {
    const updatedFeatures = { ...features };

    // auto-set type booleans
    if (currType === "All") {
      updatedFeatures["normal"] = true;
      updatedFeatures["dry"] = true;
      updatedFeatures["oily"] = true;
      updatedFeatures["combination"] = true;
    } else {
      updatedFeatures[currType.toLowerCase()] = true;
    }

    if (currAcne !== "Low") updatedFeatures["acne"] = true;

    // convert booleans -> 0/1
    Object.keys(updatedFeatures).forEach((key) => {
      updatedFeatures[key] = updatedFeatures[key] ? 1 : 0;
    });

    // ⭐ FINAL correct payload
    const payload = {
      tone: currTone,
      type: currType.toLowerCase(),
      features: {
        ...updatedFeatures,
        weight_skin: weightSkinConcern,
        weight_acne: weightAcneConcern,
        weight_price: weightPrice,
      },
    };

    console.log("FINAL PAYLOAD --->", payload);

    putForm(payload, navigate);
  };

  return (
    <Container maxWidth="xs" sx={{ marginTop: "2vh" }}>
      <Typography variant="h5" textAlign="center">
        Results
      </Typography>

      <FormControl fullWidth sx={{ marginTop: "3vh" }}>
        {/* Tone Selection */}
        <Grid container spacing={2}>
          <Grid item xs={9}>
            <InputLabel>Tone</InputLabel>
            <Select
              value={currTone}
              fullWidth
              onChange={(e) => setCurrTone(e.target.value)}
            >
              {skinToneValues.map((value) => (
                <MenuItem key={value} value={value}>
                  {value}
                </MenuItem>
              ))}
            </Select>
          </Grid>

          <Grid item xs={3}>
            <div
              style={{
                height: "3rem",
                width: "3rem",
                backgroundColor: skinToneColors[currTone - 1],
                margin: "auto",
                borderRadius: "10%",
              }}
            ></div>
          </Grid>
        </Grid>

        {/* Type */}
        <Grid marginTop="2vh">
          <FormLabel>Type</FormLabel>
          <RadioGroup
            row
            value={currType}
            onChange={(e) => setCurrType(e.target.value)}
          >
            <Grid container>
              {skinTypes.map((type) => (
                <Grid item xs={6} key={type}>
                  <FormControlLabel
                    value={type}
                    control={<Radio />}
                    label={type}
                  />
                </Grid>
              ))}
            </Grid>
          </RadioGroup>
        </Grid>

        {/* Acne */}
        <Grid marginTop="2vh">
          <FormLabel>Acne</FormLabel>
          <RadioGroup
            row
            value={currAcne}
            onChange={(e) => setAcne(e.target.value)}
          >
            {acnes.map((ac) => (
              <FormControlLabel
                key={ac}
                value={ac}
                control={<Radio />}
                label={ac}
              />
            ))}
          </RadioGroup>
        </Grid>

        {/* Other Concerns */}
        <Grid marginTop="2vh">
          <FormLabel>Other Skin Concerns</FormLabel>
          <Grid container>
            {otherConcerns.map((concern) => (
              <Grid item xs={6} key={concern}>
                <FormControlLabel
                  control={
                    <Checkbox
                      checked={features[concern]}
                      onChange={handleChange}
                      name={concern}
                    />
                  }
                  label={concern.charAt(0).toUpperCase() + concern.slice(1)}
                />
              </Grid>
            ))}
          </Grid>
        </Grid>

        {/* ⭐ NEW WEIGHT DROPDOWNS */}
        <Grid marginTop="3vh">
          <FormLabel>Weight: Skin Concern</FormLabel>
          <Select
            fullWidth
            value={weightSkinConcern}
            onChange={(e) => setWeightSkinConcern(e.target.value)}
          >
            {weightOptions.map((w) => (
              <MenuItem key={w} value={w}>
                {w}
              </MenuItem>
            ))}
          </Select>
        </Grid>

        <Grid marginTop="2vh">
          <FormLabel>Weight: Acne Concern</FormLabel>
          <Select
            fullWidth
            value={weightAcneConcern}
            onChange={(e) => setWeightAcneConcern(e.target.value)}
          >
            {weightOptions.map((w) => (
              <MenuItem key={w} value={w}>
                {w}
              </MenuItem>
            ))}
          </Select>
        </Grid>

        <Grid marginTop="2vh">
          <FormLabel>Weight: Price</FormLabel>
          <Select
            fullWidth
            value={weightPrice}
            onChange={(e) => setWeightPrice(e.target.value)}
          >
            {weightOptions.map((w) => (
              <MenuItem key={w} value={w}>
                {w}
              </MenuItem>
            ))}
          </Select>
        </Grid>

        <Grid marginTop="3vh">
          <Button variant="contained" fullWidth onClick={handleSubmit}>
            Submit
          </Button>
        </Grid>
      </FormControl>
    </Container>
  );
};

export default Form;
