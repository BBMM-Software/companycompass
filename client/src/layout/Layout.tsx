import { AppBar, Box, Toolbar, Typography } from "@mui/material";
import React from "react";
import { Outlet } from "react-router-dom";

export const Layout: React.FC = () => {
    return (
        <>
            <Box sx={{ flexGrow: 1 }}>
                <AppBar color="transparent" position="static">
                    <Toolbar>
                        <Typography
                            variant="h6"
                            component="div"
                            sx={{ flexGrow: 1 }}
                        >
                            Company Compass
                        </Typography>
                       
                    </Toolbar>
                </AppBar>
            </Box>
            <Outlet />
        </>
    );
};
