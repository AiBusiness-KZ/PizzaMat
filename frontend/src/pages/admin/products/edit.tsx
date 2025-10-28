import { Edit, useForm, useSelect } from "@refinedev/antd";
import { Form, Input, InputNumber, Switch, Upload, Select } from "antd";
import { UploadOutlined } from "@ant-design/icons";

export const ProductEdit = () => {
  const { formProps, saveButtonProps } = useForm({
    resource: "products",
  });

  const { selectProps: categorySelectProps } = useSelect({
    resource: "categories",
    optionLabel: "name",
    optionValue: "id",
  });

  return (
    <Edit saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        <Form.Item 
          label="Категория" 
          name="category_id"
          rules={[{ required: true, message: 'Пожалуйста выберите категорию' }]}
        >
          <Select {...categorySelectProps} placeholder="Выберите категорию" />
        </Form.Item>

        <Form.Item 
          label="Название" 
          name="name" 
          rules={[{ required: true, message: 'Пожалуйста введите название' }]}
        >
          <Input placeholder="Например: Маргарита" />
        </Form.Item>
        
        <Form.Item label="Описание" name="description">
          <Input.TextArea rows={4} placeholder="Описание продукта" />
        </Form.Item>
        
        <Form.Item 
          label="Базовая цена" 
          name="base_price"
          rules={[{ required: true, message: 'Пожалуйста введите цену' }]}
        >
          <InputNumber 
            min={0} 
            precision={2}
            style={{ width: '100%' }} 
            placeholder="0.00"
            addonAfter="₴"
          />
        </Form.Item>

        <Form.Item 
          label="Изображение" 
          name="image"
          valuePropName="file"
          getValueFromEvent={(e) => {
            if (Array.isArray(e)) {
              return e;
            }
            return e?.fileList?.[0]?.originFileObj;
          }}
        >
          <Upload 
            beforeUpload={() => false} 
            maxCount={1}
            listType="picture-card"
          >
            <div>
              <UploadOutlined />
              <div style={{ marginTop: 8 }}>Обновить изображение</div>
            </div>
          </Upload>
        </Form.Item>
        
        <Form.Item 
          label="Порядок сортировки" 
          name="sort_order"
        >
          <InputNumber min={0} style={{ width: '100%' }} />
        </Form.Item>
        
        <Form.Item 
          label="Активен" 
          name="is_active" 
          valuePropName="checked"
        >
          <Switch />
        </Form.Item>
      </Form>
    </Edit>
  );
};
