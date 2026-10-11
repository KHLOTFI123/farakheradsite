import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { api } from "./api";
import { useI18n } from "./i18n";
import type { SiteSettings } from "./types";

const empty: SiteSettings = { items: {}, features: [], stats: [] };
const SiteContext = createContext<SiteSettings>(empty);

export function SiteProvider({ children }: { children: ReactNode }) {
  const { lang } = useI18n();
  const [settings, setSettings] = useState<SiteSettings>(empty);

  useEffect(() => {
    api<SiteSettings>("/api/settings").then(setSettings).catch(() => undefined);
  }, [lang]);

  return <SiteContext.Provider value={settings}>{children}</SiteContext.Provider>;
}

export function useSite() {
  return useContext(SiteContext);
}
