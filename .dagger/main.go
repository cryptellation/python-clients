// A generated module for GoClient functions
//
// This module has been generated via dagger init and serves as a reference to
// basic module structure as you get started with Dagger.
//
// Two functions have been pre-created. You can modify, delete, or add to them,
// as needed. They demonstrate usage of arguments and return types using simple
// echo and grep commands. The functions can be called from the dagger CLI or
// from one of the SDKs.
//
// The first line in this comment block is a short description line and the
// rest is a long description with more detail on the module's purpose or usage,
// if appropriate. All modules should have a short description.

package main

import (
	"context"

	"github.com/cryptellation/python-clients/dagger/internal/dagger"
)

type PythonClient struct{}

// Publish a new release.
func (ci *PythonClient) PublishTag(
	ctx context.Context,
	sourceDir *dagger.Directory,
	user *string,
	token *dagger.Secret,
) error {
	// Create Git repo access
	repo, err := NewGit(ctx, NewGitOptions{
		SrcDir: sourceDir,
		User:   user,
		Token:  token,
	})
	if err != nil {
		return err
	}

	// Publish new tag
	return repo.PublishTagFromReleaseTitle(ctx)
}

// Lint runs golangci-lint on the main repo (./...) only.
// For non-Go repositories, this is a no-op.
func (ci *PythonClient) Lint(sourceDir *dagger.Directory) *dagger.Container {
	c := dag.Container().
		From("golangci/golangci-lint:v1.62.0").
		WithMountedCache("/root/.cache/golangci-lint", dag.CacheVolume("golangci-lint"))

	c = ci.withGoCodeAndCacheAsWorkDirectory(c, sourceDir)

	// For non-Go repositories, just return the container without running lint
	// as there's no Go code to lint in the main repo
	return c
}

// LintDagger runs golangci-lint on the .dagger directory only.
func (ci *PythonClient) LintDagger(sourceDir *dagger.Directory) *dagger.Container {
	c := dag.Container().
		From("golangci/golangci-lint:v1.62.0").
		WithMountedCache("/root/.cache/golangci-lint", dag.CacheVolume("golangci-lint"))

	c = ci.withGoCodeAndCacheAsWorkDirectory(c, sourceDir)

	// Lint only .dagger directory
	c = c.WithExec([]string{"sh", "-c", "cd .dagger && golangci-lint run --config ../.golangci.yml --timeout 10m ."})

	return c
}

func (ci *PythonClient) withGoCodeAndCacheAsWorkDirectory(
	c *dagger.Container,
	sourceDir *dagger.Directory,
) *dagger.Container {
	containerPath := "/go/src/github.com/cryptellation/python-clients"
	return c.
		// Add Go caches
		WithMountedCache("/root/.cache/go-build", dag.CacheVolume("gobuild")).
		WithMountedCache("/go/pkg/mod", dag.CacheVolume("gocache")).

		// Add source code
		WithMountedDirectory(containerPath, sourceDir).

		// Add workdir
		WithWorkdir(containerPath)
}
