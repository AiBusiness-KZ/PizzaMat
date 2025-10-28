import { List, useTable, EditButton, DeleteButton, CreateButton } from "@refinedev/antd";
import { Table, Space, Switch } from "antd";

export const CategoryList = () => {
  const { tableProps } = useTable({
    resource: "categories",
  });

  return (
    <List
      headerButtons={({ defaultButtons }) => (
        <>
          {defaultButtons}
          <CreateButton />
        </>
      )}
    >
      <Table {...tableProps} rowKey="id">
        <Table.Column dataIndex="id" title="ID" width={70} />
        <Table.Column dataIndex="name" title="Название" />
        <Table.Column dataIndex="description" title="Описание" />
        <Table.Column 
          dataIndex="is_active" 
          title="Активна"
          render={(value) => <Switch checked={value} disabled />}
          width={100}
        />
        <Table.Column dataIndex="sort_order" title="Порядок" width={100} />
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
