import { List, useTable, EditButton, DeleteButton, CreateButton, ImageField } from "@refinedev/antd";
import { Table, Space, Switch, Tag } from "antd";

export const ProductList = () => {
  const { tableProps } = useTable({
    resource: "products",
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
        <Table.Column 
          dataIndex="image_url" 
          title="Изображение"
          width={120}
          render={(value: string) => (
            value ? <ImageField value={`http://localhost:8000${value}`} width={80} /> : null
          )}
        />
        <Table.Column dataIndex="name" title="Название" />
        <Table.Column 
          dataIndex="category_id" 
          title="Категория ID"
          width={120}
        />
        <Table.Column 
          dataIndex="base_price" 
          title="Цена"
          width={100}
          render={(value: number) => `${value} ₴`}
        />
        <Table.Column 
          dataIndex="is_active" 
          title="Активен"
          width={100}
          render={(value: boolean) => (
            value ? <Tag color="green">Да</Tag> : <Tag color="red">Нет</Tag>
          )}
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
