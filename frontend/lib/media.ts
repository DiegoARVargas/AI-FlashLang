export function getMediaUrl(path: string): string {
    const baseUrl = (process.env.NEXT_PUBLIC_BACKEND_URL ?? '').replace(/\/api\/?$/, '');
    return `${baseUrl}${path}`;
  }