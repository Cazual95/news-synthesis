import * as React from "react";
import * as ReactDOM from "react-dom/client";
import '@radix-ui/themes/styles.css';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Root from "./routes/root";
import ErrorPage from "./error-page";
import LoginPage from "./routes/login";
import RegisterPage from "./routes/register";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: 'register',
    element: <RegisterPage />
  }
]);

// @ts-ignore
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);