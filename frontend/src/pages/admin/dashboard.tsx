import { Card, Col, Row, Statistic } from "antd";
import { ShoppingCartOutlined, AppstoreOutlined, EnvironmentOutlined, FileTextOutlined } from "@ant-design/icons";

export const Dashboard = () => {
  return (
    <div style={{ padding: '24px' }}>
      <h1>Dashboard</h1>
      <Row gutter={16} style={{ marginTop: '24px' }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Категории"
              value={0}
              prefix={<AppstoreOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Продукты"
              value={0}
              prefix={<ShoppingCartOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Локации"
              value={0}
              prefix={<EnvironmentOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Заказы"
              value={0}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};
