// /frontend/schemas/zodSchemas.ts
import { z } from 'zod';

export const editProfileSchema = z.object({
  display_name: z
    .string()
    .min(2, 'Debe tener al menos 2 caracteres')
    .max(50, 'Máximo 50 caracteres'),
  preferred_language: z.enum(['en', 'es', 'fr'], {
    errorMap: () => ({ message: 'Idioma inválido' }),
  }),
});
