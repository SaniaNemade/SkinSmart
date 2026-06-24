import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadImage } from '../controllers/actions';
import WebcamCapture from './Components/webCam';

// MUI
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';
import Button from '@mui/material/Button';

function ImageInput() {
  const [landingPage, setLandingPage] = useState(true);
  const navigate = useNavigate();

  return (
    <Container maxWidth="xs" sx={{ padding: 0 }}>
      <Grid container justifyContent="center" spacing={1}>
        {landingPage ? (
          <Grid item xs={6} sx={{ margin: "40vh auto" }} textAlign="center">
            <PhotoCameraIcon sx={{ fontSize: "5em" }} />
            <Button
              onClick={() => setLandingPage(false)}
              variant="contained"
              fullWidth
            >
              Take a photo
            </Button>
          </Grid>
        ) : (
          <WebcamCapture navigate={navigate} uploadImage={UploadImage} />
        )}
      </Grid>
    </Container>
  );
}

export default ImageInput;
