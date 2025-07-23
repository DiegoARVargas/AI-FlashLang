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

  // ✅ Esquema para register
export const registerSchema = z
  .object({
    username: z
      .string()
      .min(3, 'El nombre de usuario debe tener al menos 3 caracteres')
      .max(30, 'Máximo 30 caracteres'),
    email: z.string().email('Correo electrónico inválido'),
    display_name: z
      .string()
      .min(2, 'Debe tener al menos 2 caracteres')
      .max(50, 'Máximo 50 caracteres'),
    preferred_language: z.enum(['en', 'es', 'fr'], {
      errorMap: () => ({ message: 'Idioma inválido' }),
    }),
    password: z
      .string()
      .min(8, 'La contraseña debe tener al menos 8 caracteres'),
    confirm_password: z
      .string()
      .min(8, 'La confirmación debe tener al menos 8 caracteres'),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: 'Las contraseñas no coinciden',
    path: ['confirm_password'],
  });

  // ✅ Esquema para login
export const loginSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

