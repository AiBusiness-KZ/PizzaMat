/**
 * Telegram WebApp type definitions
 */

interface TelegramWebApp {
  /**
   * A method that informs the Telegram app that the Web App is ready to be displayed
   */
  ready: () => void;
  
  /**
   * A method that expands the Web App to the maximum available height
   */
  expand: () => void;
  
  /**
   * A string with raw data transferred to the Web App, convenient for validating data
   */
  initData: string;
  
  /**
   * An object with input data transferred to the Web App
   */
  initDataUnsafe: {
    query_id?: string;
    user?: {
      id: number;
      first_name: string;
      last_name?: string;
      username?: string;
      language_code?: string;
    };
    auth_date: number;
    hash: string;
  };
  
  /**
   * The color scheme currently used in the Telegram app
   */
  colorScheme: 'light' | 'dark';
  
  /**
   * An object containing the current theme settings used in the Telegram app
   */
  themeParams: {
    bg_color?: string;
    text_color?: string;
    hint_color?: string;
    link_color?: string;
    button_color?: string;
    button_text_color?: string;
  };
  
  /**
   * True if the Web App is expanded to the maximum available height
   */
  isExpanded: boolean;
  
  /**
   * The current height of the visible area of the Web App
   */
  viewportHeight: number;
  
  /**
   * The height of the visible area of the Web App in its last stable state
   */
  viewportStableHeight: number;
}

interface Window {
  Telegram?: {
    WebApp: TelegramWebApp;
  };
}
