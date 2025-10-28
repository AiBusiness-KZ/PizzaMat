import { Refine } from "@refinedev/core";
import { RefineThemes, ThemedLayoutV2, notificationProvider } from "@refinedev/antd";
import routerProvider, { NavigateToResource } from "@refinedev/react-router-v6";
import { BrowserRouter, Routes, Route, Outlet } from "react-router-dom";
import { ConfigProvider, App as AntdApp } from "antd";
import { 
  AppstoreOutlined, 
  ShoppingCartOutlined, 
  EnvironmentOutlined, 
  SettingOutlined 
} from "@ant-design/icons";

import "@refinedev/antd/dist/reset.css";

import { dataProvider } from "./providers/dataProvider";
import HomePage from "./pages/Home";

// Admin pages
import { Dashboard } from "./pages/admin/dashboard";
import { CategoryList } from "./pages/admin/categories/list";
import { CategoryCreate } from "./pages/admin/categories/create";
import { CategoryEdit } from "./pages/admin/categories/edit";
import { ProductList } from "./pages/admin/products/list";
import { ProductCreate } from "./pages/admin/products/create";
import { ProductEdit } from "./pages/admin/products/edit";
import { LocationList } from "./pages/admin/locations/list";
import { LocationCreate } from "./pages/admin/locations/create";
import { LocationEdit } from "./pages/admin/locations/edit";
import { SettingsEdit } from "./pages/admin/settings/edit";

export default function App() {
  return (
    <BrowserRouter>
      <ConfigProvider theme={RefineThemes.Blue}>
        <AntdApp>
          <Refine
            dataProvider={dataProvider}
            routerProvider={routerProvider}
            notificationProvider={notificationProvider}
            resources={[
              {
                name: "dashboard",
                list: "/admin",
                meta: {
                  label: "Dashboard",
                  icon: <AppstoreOutlined />,
                },
              },
              {
                name: "categories",
                list: "/admin/categories",
                create: "/admin/categories/create",
                edit: "/admin/categories/edit/:id",
                meta: {
                  label: "Категории",
                  icon: <AppstoreOutlined />,
                },
              },
              {
                name: "products",
                list: "/admin/products",
                create: "/admin/products/create",
                edit: "/admin/products/edit/:id",
                meta: {
                  label: "Продукты",
                  icon: <ShoppingCartOutlined />,
                },
              },
              {
                name: "locations",
                list: "/admin/locations",
                create: "/admin/locations/create",
                edit: "/admin/locations/edit/:id",
                meta: {
                  label: "Локации",
                  icon: <EnvironmentOutlined />,
                },
              },
              {
                name: "settings",
                list: "/admin/settings",
                meta: {
                  label: "Настройки",
                  icon: <SettingOutlined />,
                },
              },
            ]}
            options={{
              syncWithLocation: true,
              warnWhenUnsavedChanges: true,
            }}
          >
            <Routes>
              {/* Client route */}
              <Route path="/" element={<HomePage />} />
              
              {/* Admin routes */}
              <Route
                path="/admin"
                element={
                  <ThemedLayoutV2>
                    <Outlet />
                  </ThemedLayoutV2>
                }
              >
                <Route index element={<Dashboard />} />
                
                <Route path="categories">
                  <Route index element={<CategoryList />} />
                  <Route path="create" element={<CategoryCreate />} />
                  <Route path="edit/:id" element={<CategoryEdit />} />
                </Route>

                <Route path="products">
                  <Route index element={<ProductList />} />
                  <Route path="create" element={<ProductCreate />} />
                  <Route path="edit/:id" element={<ProductEdit />} />
                </Route>

                <Route path="locations">
                  <Route index element={<LocationList />} />
                  <Route path="create" element={<LocationCreate />} />
                  <Route path="edit/:id" element={<LocationEdit />} />
                </Route>

                <Route path="settings">
                  <Route index element={<SettingsEdit />} />
                </Route>
              </Route>

              {/* Catch all */}
              <Route path="*" element={<NavigateToResource resource="dashboard" />} />
            </Routes>
          </Refine>
        </AntdApp>
      </ConfigProvider>
    </BrowserRouter>
  );
}
