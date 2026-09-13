/**
 * Central API base URL config.
 * In development: empty string → Vite dev proxy handles /api/* → localhost:8000
 * In production: set VITE_API_BASE_URL in Cloudflare Pages env vars
 *   e.g. VITE_API_BASE_URL=https://mythos-atlas-three.vercel.app
 */
export const API_BASE = import.meta.env.VITE_API_BASE_URL ?? '';
