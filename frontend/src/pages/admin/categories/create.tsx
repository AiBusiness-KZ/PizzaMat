import { Create, useForm } from "@refinedev/antd";
import { Form, Input, InputNumber, Switch } from "antd";

export const CategoryCreate = () => {
  const { formProps, saveButtonProps } = useForm({
    resource: "categories",
  });

  return (
    <Create saveButtonProps={saveButtonProps}>
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
          initialValue={0}
        >
          <InputNumber min={0} style={{ width: '100%' }} />
        </Form.Item>
        
        <Form.Item 
          label="Активна" 
          name="is_active" 
          valuePropName="checked" 
          initialValue={true}
        >
          <Switch />
        </Form.Item>
      </Form>
    </Create>
  );
};
