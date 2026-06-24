import React, { useState, useEffect } from 'react';

// MUI
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import FormLabel from '@mui/material/FormLabel';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

import ProductCard from './Components/ProductCard'
import { useLocation } from 'react-router';


const Recommendations = () => {
    const {state} = useLocation();
    const {data} = state; 
    const {general, makeup, graphs} = data;
    
    return <>
        <Container sx={{ marginTop: "2vh", padding: 1 }} alignitems="center" width="inherit">
            
            {/* Analysis Graphs Section */}
            {graphs && (
                <Box sx={{ marginBottom: 4 }}>
                    <Typography gutterBottom variant="h4" component="div" marginTop="2vh" textAlign="center">
                        Recommendation Analysis
                    </Typography>
                    
                    <Grid container spacing={2} sx={{ marginTop: 2 }}>
                        {/* Sensitivity Graph */}
                        <Grid item xs={12}>
                            <Paper elevation={3} sx={{ padding: 2 }}>
                                <Typography variant="h6" component="div" textAlign="center" color="text.secondary" gutterBottom>
                                    Sensitivity Analysis
                                </Typography>
                                <Typography variant="body2" component="div" textAlign="center" color="text.secondary" sx={{ marginBottom: 2 }}>
                                    How changes in weight preferences affect product scores
                                </Typography>
                                <Box sx={{ 
                                    display: 'flex', 
                                    justifyContent: 'center', 
                                    alignItems: 'center',
                                    width: '100%'
                                }}>
                                    <img 
                                        src={graphs.sensitivity_graph} 
                                        alt="Sensitivity Analysis" 
                                        style={{ 
                                            maxWidth: '100%', 
                                            height: 'auto',
                                            borderRadius: '4px'
                                        }} 
                                    />
                                </Box>
                            </Paper>
                        </Grid>
                        
                        {/* Utility Graph */}
                        <Grid item xs={12}>
                            <Paper elevation={3} sx={{ padding: 2 }}>
                                <Typography variant="h6" component="div" textAlign="center" color="text.secondary" gutterBottom>
                                    Utility Analysis
                                </Typography>
                                <Typography variant="body2" component="div" textAlign="center" color="text.secondary" sx={{ marginBottom: 2 }}>
                                    Distribution of product scores based on your preferences
                                </Typography>
                                <Box sx={{ 
                                    display: 'flex', 
                                    justifyContent: 'center', 
                                    alignItems: 'center',
                                    width: '100%'
                                }}>
                                    <img 
                                        src={graphs.utility_graph} 
                                        alt="Utility Analysis" 
                                        style={{ 
                                            maxWidth: '100%', 
                                            height: 'auto',
                                            borderRadius: '4px'
                                        }} 
                                    />
                                </Box>
                            </Paper>
                        </Grid>
                    </Grid>
                </Box>
            )}

            {/* Skin Care Products Section */}
            <Typography gutterBottom variant="h4" component="div" marginTop="4vh" textAlign="center">
                Skin care
            </Typography>
            {Object.keys(general).map((type, products) => {
                return (
                    <div key={type}>
                        <Typography gutterBottom variant="h5" component="div" marginTop="2vh" color="text.secondary">
                            {type}
                        </Typography>
                        <Grid container spacing={1}>
                            {general[type].slice(0,4).map((prod, index) => {
                                return <Grid item xs={6} md={3} key={index}>
                                    <ProductCard
                                        name={prod.name}
                                        brand={prod.brand}
                                        image={prod.img}
                                        price={prod.price}
                                        url={prod.url}
                                        concern={prod.concern} />
                                </Grid>
                            })}
                        </Grid>
                    </div>
                )
            })}

            {/* Make Up Products Section */}
            <Typography gutterBottom variant="h4" component="div" marginTop="4vh" textAlign="center">
                Make up
            </Typography>

            <FormLabel component="legend">{ }</FormLabel>
            <div>
                <Grid container spacing={1}>
                    {makeup.map((prod, index) => {
                        return <Grid item xs={6} md={3} key={index}>
                            <ProductCard
                                name={prod.name}
                                brand={prod.brand}
                                image={prod.img}
                                price={prod.price}
                                url={prod.url}
                                concern={prod.concern} />
                        </Grid>
                    })}
                </Grid>
            </div>
        </Container>
    </>
};

export default Recommendations;