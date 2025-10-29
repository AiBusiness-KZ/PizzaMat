import { Create, useForm } from "@refinedev/antd";
import { Form, Input, Switch } from "antd";

export const CityCreate = () => {
  const { formProps, saveButtonProps } = useForm({
    resource: "cities",
  });

  return (
    <Create saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        <Form.Item 
          label="Название города" 
          name="name" 
          rules={[{ required: true, message: 'Пожалуйста введите название города' }]}
        >
          <Input placeholder="Например: Київ" />
        </Form.Item>
        
        <Form.Item 
          label="Активен" 
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
