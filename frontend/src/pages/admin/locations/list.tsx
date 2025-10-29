import { List, useTable, EditButton, DeleteButton, CreateButton } from "@refinedev/antd";
import { Table, Space, Tag } from "antd";

export const LocationList = () => {
  const { tableProps } = useTable({
    resource: "locations",
  });

  return (
    <List>
      <Table {...tableProps} rowKey="id">
        <Table.Column dataIndex="id" title="ID" width={70} />
        <Table.Column dataIndex="name" title="Название" />
        <Table.Column dataIndex="city_name" title="Город" width={150} />
        <Table.Column dataIndex="address" title="Адрес" />
        <Table.Column dataIndex="working_hours" title="Часы работы" width={150} />
        <Table.Column 
          dataIndex="is_active" 
          title="Активна"
          width={100}
          render={(value: boolean) => (
            value ? <Tag color="green">Да</Tag> : <Tag color="red">Нет</Tag>
          )}
        />
        <Table.Column
          title="Действия"
          width={150}
          render={(_, record: any) => (
            <Space>
              <EditButton size="small" recordItemId={record.id} />
              <DeleteButton size="small" recordItemId={record.id} />
            </Space>
          )}
        />
      </Table>
    </List>
  );
};
