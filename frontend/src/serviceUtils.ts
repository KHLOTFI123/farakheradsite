import type { ServiceDetails, ServiceItem } from "./types";

export function parseServiceDetails(raw?: string): ServiceDetails {
  try {
    return JSON.parse(raw || "{}") as ServiceDetails;
  } catch {
    return {};
  }
}

export function isFeaturedService(service: ServiceItem) {
  const details = parseServiceDetails(service.details);
  return Boolean(details.featured || service.slug === "devops" || service.slug === "mlops");
}
