import { Edit, useForm, useSelect } from "@refinedev/antd";
import { Form, Input, Switch, Select } from "antd";

export const LocationEdit = () => {
  const { formProps, saveButtonProps } = useForm({
    resource: "locations",
  });

  const { selectProps: citySelectProps } = useSelect({
    resource: "cities",
    optionLabel: "name",
    optionValue: "id",
  });

  return (
    <Edit saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        <Form.Item 
          label="Город" 
          name="city_id"
          rules={[{ required: true, message: 'Пожалуйста выберите город' }]}
        >
          <Select {...citySelectProps} placeholder="Выберите город" />
        </Form.Item>

        <Form.Item 
          label="Название" 
          name="name" 
          rules={[{ required: true, message: 'Пожалуйста введите название' }]}
        >
          <Input placeholder="Например: ТРЦ Глобус" />
        </Form.Item>
        
        <Form.Item 
          label="Адрес" 
          name="address"
          rules={[{ required: true, message: 'Пожалуйста введите адрес' }]}
        >
          <Input.TextArea rows={2} placeholder="Полный адрес локации" />
        </Form.Item>
        
        <Form.Item 
          label="Часы работы" 
          name="working_hours"
        >
          <Input placeholder="Например: 09:00-22:00" />
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
