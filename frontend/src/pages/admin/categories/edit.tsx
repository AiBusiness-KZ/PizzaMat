import { Edit, useForm } from "@refinedev/antd";
import { Form, Input, InputNumber, Switch } from "antd";

export const CategoryEdit = () => {
  const { formProps, saveButtonProps, queryResult } = useForm({
    resource: "categories",
  });

  return (
    <Edit saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        <Form.Item 
          label="Название" 
          name="name" 
          rules={[{ required: true, message: 'Пожалуйста введите название' }]}
        >
          <Input placeholder="Например: Пицца" />
        </Form.Item>
        
        <Form.Item label="Описание" name="description">
          <Input.TextArea rows={4} placeholder="Описание категории" />
        </Form.Item>
        
        <Form.Item 
          label="Порядок сортировки" 
          name="sort_order"
        >
          <InputNumber min={0} style={{ width: '100%' }} />
        </Form.Item>
        
        <Form.Item 
          label="Активна" 
          name="is_active" 
          valuePropName="checked"
        >
          <Switch />
        </Form.Item>
      </Form>
    </Edit>
  );
};
