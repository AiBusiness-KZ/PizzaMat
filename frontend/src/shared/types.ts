import z from "zod";

// Схемы категорий
export const CategorySchema = z.object({
  id: z.number(),
  category_id: z.string(),
  name: z.string(),
  display_order: z.number().default(0),
  is_active: z.boolean().default(true),
  created_at: z.string(),
  updated_at: z.string(),
});

export type Category = z.infer<typeof CategorySchema>;

// Схемы опций продуктов
export const ProductOptionSchema = z.object({
  type: z.string(), // "Размер", "Добавка"
  name: z.string(),
  price_modifier: z.number(),
});

export type ProductOption = z.infer<typeof ProductOptionSchema>;

// Схемы продуктов
export const ProductSchema = z.object({
  id: z.number(),
  product_id: z.string().nullable(),
  category_id: z.number().nullable(),
  name: z.string(),
  description: z.string().nullable(),
  base_price: z.number(),
  photo_url: z.string().nullable(),
  options: z.array(ProductOptionSchema).nullable(),
  is_available: z.boolean().default(true),
  display_order: z.number().default(0),
  created_at: z.string(),
  updated_at: z.string(),
});

export type Product = z.infer<typeof ProductSchema>;

// Схемы точек выдачи
export const PickupLocationSchema = z.object({
  id: z.number(),
  location_id: z.string(),
  city_id: z.number(),
  name: z.string(),
  address: z.string(),
  city: z.string(),
  is_active: z.boolean().default(true),
  created_at: z.string(),
  updated_at: z.string(),
});

export type PickupLocation = z.infer<typeof PickupLocationSchema>;

// Схемы элементов заказа
export const OrderItemSchema = z.object({
  product_id: z.string(),
  product_name: z.string(),
  quantity: z.number(),
  selected_options: z.array(ProductOptionSchema),
  price_per_unit: z.number(),
  total_price: z.number(),
});

export type OrderItem = z.infer<typeof OrderItemSchema>;

// Схемы данных чека
export const ReceiptDataSchema = z.object({
  verification_status: z.enum(["automatic", "manual", "rejected"]),
  amount: z.number().nullable(),
  bank: z.string().nullable(),
  date_time: z.string().nullable(),
  transaction_id: z.string().nullable(),
  photo_url: z.string().nullable(),
});

export type ReceiptData = z.infer<typeof ReceiptDataSchema>;

// Схемы заказов
export const OrderSchema = z.object({
  id: z.number(),
  order_id: z.string(),
  user_telegram_id: z.string().nullable(),
  user_telegram_name: z.string().nullable(),
  status: z.enum([
    "pending_payment",
    "paid",
    "preparing",
    "ready",
    "completed",
    "cancelled",
    "receipt_verification"
  ]),
  total_amount: z.number(),
  currency: z.string().default("UAH"),
  order_details: z.array(OrderItemSchema),
  pickup_code: z.string(),
  pickup_location_id: z.string(),
  pickup_location_name: z.string(),
  receipt_data: ReceiptDataSchema.nullable(),
  manager_comment: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});

export type Order = z.infer<typeof OrderSchema>;

// API схемы для создания заказа
export const CreateOrderRequestSchema = z.object({
  user_telegram_id: z.string().optional(),
  user_telegram_name: z.string().optional(),
  order_items: z.array(OrderItemSchema),
  pickup_location_id: z.string(),
});

export type CreateOrderRequest = z.infer<typeof CreateOrderRequestSchema>;
