# GR Web Template

This template allows you to get up and running building internal team web applications super quickly. It's built with React, Typescript, and Tailwind CSS with shadcn/ui serving as the primary component library. Vite is configured as the build server.

## Getting started

You should download this entire repository and copy it into your project. If your internal application features a backend (it should, so you can leverage Sentinel OAuth), place everything under the `web/` directory. Else, you can just put everything in your project's root directory.

Make sure you have node.js and npm installed.

First, install the dependencies:

```bash
npm i
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) with your browser to see the result.

## Integrating Sentinel

Integrating Sentinel is as simple as registering a new application, and updating the `SENTINEL_CLIENT_ID` and `BACKEND_URL` values in `src/consts/config.tsx`.

Check out the Sentinel documentation [here](https://wiki.gauchoracing.com/books/sentinel) for more info.

## Linting & Formatting

ESLint and Prettier are preconfiured in this template to enforce our team's lint standards. You can use the following commands to test locally.

```
npm run lint

npm run check
```

> [!TIP]
> You can use `npm run format` to fix any prettier lint errors you have.

## Resources

To learn more about React, Typescript, Tailwind, or Shadcn, take a look at the following resources:

- React.js Docs - https://react.dev/learn
- Vite Docs - https://vite.dev/guide/
- Typescript Docs - https://www.typescriptlang.org/docs/
- Tailwind CSS Docs - https://tailwindcss.com/docs/installation
- shadcn/ui Docs - https://ui.shadcn.com/docs

## Contributing

If you have a suggestion that would make this template better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b gh-username/my-amazing-feature`)
3. Commit your Changes (`git commit -m 'Add my amazing feature'`)
4. Push to the Branch (`git push origin gh-username/my-amazing-feature`)
5. Open a Pull Request