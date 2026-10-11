import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { LocaleProvider } from "./i18n";
import { SiteProvider } from "./siteContext";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <LocaleProvider>
        <SiteProvider>
          <App />
        </SiteProvider>
      </LocaleProvider>
    </BrowserRouter>
  </React.StrictMode>,
);
