# Performance Budget and Core Web Vitals

A high-performing landing page converts visitors into customers. Slow pages lose leads before they read the headline.

Target Benchmarks:
- LCP (Largest Contentful Paint): < 2.5 seconds (optimized with Next.js `next/image` and modern webp/avif formats).
- INP (Interaction to Next Paint): < 200 ms (lightweight JS, no render-blocking scripts).
- CLS (Cumulative Layout Shift): <= 0.1 (explicit width and height on images and banners).

Use `check_performance_budget` to audit estimated JS bundle size and animation counts before deployment.
