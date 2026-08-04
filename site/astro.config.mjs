import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightThemeBlack from 'starlight-theme-black';

export default defineConfig({
  site: 'https://nkai-share.github.io',
  base: '/nankai-ai-Datashare',
  trailingSlash: 'always',
  integrations: [
    starlight({
      title: 'NKAI DataShare',
      description: '南开大学人工智能学院课程资料共享平台',
      disable404Route: true,
      favicon: '/nankai-ai-Datashare/favicon.svg',
      logo: {
        src: './src/assets/logo.svg',
        replacesTitle: false,
      },
      plugins: [starlightThemeBlack({})],
      defaultLocale: 'root',
      locales: {
        root: { label: '简体中文', lang: 'zh-CN' },
      },
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/nkai-share/nankai-ai-Datashare',
        },
      ],
      customCss: ['./src/styles/tokens.css', './src/styles/global.css'],
      sidebar: [
        { label: '资料平台', items: [
          { label: '资料大厅', link: '/resources/' },
          { label: '投稿指南', link: '/contribute/' },
          { label: '关于项目', link: '/about/' },
        ] },
      ],
    }),
  ],
});
