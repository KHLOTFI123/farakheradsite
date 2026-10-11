export type Slide = {
  id: number;
  title: string;
  subtitle: string;
  description: string;
  image_url: string;
  cta_primary_text: string;
  cta_primary_link: string;
  cta_secondary_text: string;
  cta_secondary_link: string;
  sort_order: number;
  is_active: boolean;
};

export type ProductBlock = {
  title: string;
  text: string;
};

export type ProductFaq = {
  q: string;
  a: string;
};

export type ProductDetails = {
  tagline?: string;
  related?: string[];
  features?: ProductBlock[];
  benefits?: ProductBlock[];
  audiences?: string[];
  steps?: ProductBlock[];
  faqs?: ProductFaq[];
};

export type Product = {
  id: number;
  title: string;
  slug: string;
  summary: string;
  description: string;
  image_url: string;
  details?: string;
  sort_order: number;
  is_active: boolean;
};

export type ServiceBlock = {
  title: string;
  text?: string;
};

export type ServiceDetails = {
  featured?: boolean;
  kicker?: string;
  lead?: string;
  intro_title?: string;
  intro?: string[];
  offerings_title?: string;
  offerings_lead?: string;
  offerings?: ServiceBlock[];
  why_title?: string;
  why_lead?: string;
  why?: ServiceBlock[];
  cta_lead?: string;
  cta_text?: string;
};

export type ServiceItem = {
  id: number;
  title: string;
  slug: string;
  description: string;
  icon: string;
  image_url?: string;
  details?: string;
  sort_order: number;
};

export type Feature = {
  id: number;
  title: string;
  description: string;
  icon: string;
  sort_order: number;
};

export type Stat = {
  id: number;
  title: string;
  description: string;
  icon: string;
  sort_order: number;
};

export type Article = {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  image_url: string;
  published_at: string;
};

export type SiteSettings = {
  items: Record<string, string>;
  features: Feature[];
  stats: Stat[];
};

export type Message = {
  id: number;
  name: string;
  email: string;
  phone: string;
  subject: string;
  body: string;
  is_read: boolean;
  created_at: string;
};
