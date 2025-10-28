import { Edit, useForm } from "@refinedev/antd";
import { Form, Input, Upload } from "antd";
import { UploadOutlined } from "@ant-design/icons";

export const SettingsEdit = () => {
  const { formProps, saveButtonProps } = useForm({
    resource: "settings",
    id: 1,
  });

  return (
    <Edit saveButtonProps={saveButtonProps}>
      <Form {...formProps} layout="vertical">
        <Form.Item 
          label="Название сайта" 
          name="site_name"
        >
          <Input placeholder="PizzaMat" />
        </Form.Item>
        
        <Form.Item label="Описание" name="site_description">
          <Input.TextArea rows={3} placeholder="Описание сайта" />
        </Form.Item>

        <Form.Item 
          label="Логотип" 
          name="logo"
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
              <div style={{ marginTop: 8 }}>Загрузить лого</div>
            </div>
          </Upload>
        </Form.Item>
        
        <Form.Item label="Телефон" name="phone">
          <Input placeholder="+380501234567" />
        </Form.Item>
        
        <Form.Item label="Email" name="email">
          <Input type="email" placeholder="info@pizzamat.com" />
        </Form.Item>
        
        <Form.Item label="Адрес" name="address">
          <Input.TextArea rows={2} placeholder="Адрес компании" />
        </Form.Item>

        <Form.Item label="Telegram Bot Token" name="bot_token">
          <Input.Password placeholder="7123456789:AAHdq..." />
        </Form.Item>

        <Form.Item label="Manager Channel ID" name="manager_channel_id">
          <Input placeholder="-1001234567890" />
        </Form.Item>

        <Form.Item label="Admin Telegram IDs" name="admin_telegram_ids">
          <Input placeholder="123456789,987654321" />
        </Form.Item>

        <Form.Item label="OpenAI API Key" name="openai_api_key">
          <Input.Password placeholder="sk-..." />
        </Form.Item>

        <Form.Item label="n8n URL" name="n8n_url">
          <Input placeholder="https://n8n.example.com" />
        </Form.Item>

        <Form.Item label="n8n Webhook Secret" name="n8n_webhook_secret">
          <Input.Password placeholder="webhook secret" />
        </Form.Item>
      </Form>
    </Edit>
  );
};
