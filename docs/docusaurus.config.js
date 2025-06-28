const { themes } = require('prism-react-renderer');

module.exports = {
  title: 'CraftX.py',
  tagline: 'Python-native intelligence, modular by design.',
  url: 'https://craftx.dev',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/craftx-monogram.svg',
  
  organizationName: 'davidanderson01',
  projectName: 'craftxpy',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/davidanderson01/craftxpy/tree/main/docs/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/davidanderson01/craftxpy/tree/main/docs/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'CraftX.py',
      logo: {
        alt: 'CraftX.py Logo',
        src: 'img/craftx-monogram.svg',
      },
      items: [
        {
          type: 'doc',
          docId: 'intro',
          position: 'left',
          label: 'Docs',
        },
        {
          to: '/blog',
          label: 'Blog',
          position: 'left'
        },
        {
          href: 'https://github.com/davidanderson01/craftxpy',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Getting Started',
              to: '/docs/intro',
            },
            {
              label: 'API Reference',
              to: '/docs/api',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub Discussions',
              href: 'https://github.com/davidanderson01/craftxpy/discussions',
            },
            {
              label: 'Discord',
              href: 'https://discord.gg/craftxpy',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/davidanderson01/craftxpy',
            },
            {
              label: 'PyPI',
              href: 'https://pypi.org/project/craftxpy',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} CraftX.py. Built with Docusaurus.`,
      logo: {
        alt: 'CraftX.py Logo',
        src: 'img/craftx-logo.svg',
        href: 'https://craftx.dev',
        width: 120,
      },
    },
    prism: {
      theme: themes.github,
      darkTheme: themes.dracula,
      additionalLanguages: ['python', 'bash', 'json'],
    },
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
  },
};
