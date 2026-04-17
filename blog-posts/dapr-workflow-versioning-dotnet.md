---
prompt: "Create a blog post about Dapr Workflow Versioning in .NET. Use the EnterpriseDiagnostics Aspire application in C:\\dev\\diagrid-labs\\dapr-workflow-versioning\\EnterpriseDiagnostics. Use the DiagnosticsWorkflow.cs and use the code snippet 01-add-activity.txt to indicate how a version patch is working. Use DiagnosticsWorkflowV2.cs to indicate how a named workflow version is working. Use Program.cs for code blocks about builder.Services.AddDaprWorkflow(options =>{...}) and builder.Services.AddDaprWorkflowVersioning();"
type: How-to
audience: .NET developers already using Dapr Workflow who want to ensure not to introduce breaking changes in their production workflows
intent: Understand the difference between patching workflows for small changes, and named workflows for big changes
ctas:
  - Sign up for a free Catalyst account at https://catalyst.diagrid.io/
  - Join the Dapr Discord at http://bit.ly/dapr-discord
key_points:
  - Old workflow state of in-flight workflows causes issues when a new workflow has been deployed with breaking changes
  - Refer to the EnterpriseDiagnostics demo with code blocks
  - Include step by step instructions to run the solution
  - Show a version patch with IsPatched
  - Show a named workflow version (V2)
  - Show AddDaprWorkflow and AddDaprWorkflowVersioning configuration
---

## Title Suggestions

1. How to Version .NET Dapr Workflows in Aspire Without Breaking In-Flight Instances
2. How to Evolve Dapr Workflows Safely with Patches and Named Versions
3. How to Ship Changes to Running Dapr Workflows in .NET
4. How to Handle Breaking Changes in Dapr Workflows with Versioning
5. How to Keep Running Dapr Workflows Healthy When You Deploy New Code

---

# How to Version .NET Dapr Workflows in Aspire Without Breaking In-Flight Instances

## Introduction

You have a Dapr Workflow running in production and a change request lands. Maybe an activity needs to be added, or the control flow needs a more substantial rework. You cannot just redeploy and hope for he best: in-flight workflow instances replay their saved history against the updated workflow code, and any non-deterministic change will fail the replay.

This post shows you how to evolve your .NET Dapr Workflows safely using two complementary techniques. Patches for small, additive changes, and named workflow versions for larger, breaking changes. Using the EnterpriseDiagnostics Aspire demo as a running example, you will see when each approach applies, how to wire it up, and how to verify it behaves correctly.

## The In-Flight Workflow Problem

Dapr Workflow is durable because the engine appends every activity call, with inputs and outputs, durable timers, and child workflow calls to the workflow state store. When the workflow application restarts, for instance after a new deployment code, the Dapr Workflow engine replays that history against your updated workflow code to rebuild the in-memory state and continue where it left off.

Replay only works if the code is deterministic. If the new code calls a different activity, reorders steps, or inserts a branch before a completed step, the replayed history stops matching what the workflow expects. The instance fails, gets stuck, or finishes with silently incorrect state.

The question is not whether you can change the workflow code, but how to change it without breaking instances that are already running. Dapr Workflow versioning solves this.

## The EnterpriseDiagnostics demo

The EnterpriseDiagnostics demo is a .NET 10 Aspire application that runs a Dapr Workflow to perform diagnostics for the starship USS Enterprise. It analyzes the hull, warp core, and security protocols, then generates recommendations and notifies the bridge. Each activity in the workflow is using the Dapr Conversation API to create the activity output. All the code is available in [this GitHub repo](https://github.com/diagrid-labs/dapr-workflow-versioning).

Before you run the demo, make sure you have the following installed:

- [Docker](https://www.docker.com/products/docker-desktop/) or [Podman](https://podman.io/docs/installation)
- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0)
- [Aspire CLI](https://aspire.dev/get-started/install-cli/)
- [Dapr CLI](https://docs.dapr.io/getting-started/install-dapr-cli/) (and initialized with `dapr init`)
- An [Anthropic](https://claude.com/platform/api) API key

With the prerequisites in place, download and start the solution:

1. Clone the [repository](https://github.com/diagrid-labs/dapr-workflow-versioning) and open the `dapr-workflow-versioning` folder.
2. Add your Anthropic API key to `EnterpriseDiagnostics.AppHost/Resources/conversation.yaml`.
3. Use the terminal to navigate to the `EnterpriseDiagnostics` folder and run `aspire run`. Aspire starts a Valkey container for workflow state, the ApiService (with the workflow definition) with a Dapr sidecar, and the [Diagrid Dev Dashboard](https://docs.diagrid.io/develop/diagrid-dashboard) container.
4. Use the terminal to start a workflow by sending a POST request to the `/start` endpoint:

  ```shell
  curl -X POST http://localhost:5467/start \
    -H "Content-Type: application/json" \
    -d '{
      "id": "diag-001",
      "shipName": "USS Enterprise NCC-1701-D",
      "diagnosticsDate": "2370-04-08",
      "engineerName": "Geordi La Forge"
    }'
  ```

5. Open the Diagrid Dev Dashboard from the Aspire resources page to watch the workflow execute.
6. To simulate the effect of in-flight workflows and changing versions, pause the workflow before it finishes by making a POST request to the `/pause` endpoint:

  ```shell
  curl -X POST http://localhost:5467/pause/diag-001
  ```

  The workflow should have the `suspended` status now.

7. Stop the Aspire solution using `CTRL+C` in the terminal where Aspire is running.

## Inspect the Workflow & Activity registration

Dapr Workflow configuration lives in `Program.cs`:

```csharp
builder.Services.AddDaprWorkflow(options =>
{
    options.RegisterActivity<AnalyzeHullActivity>();
    options.RegisterActivity<AnalyzeWarpCoreActivity>();
    options.RegisterActivity<AnalyzeSecuritySystemsActivity>();
    options.RegisterActivity<GenerateRecommendationsActivity>();
    options.RegisterActivity<NotifyBridgeActivity>();
});
builder.Services.AddDaprWorkflowVersioning();
```

- `AddDaprWorkflow` registers each activity with the Dapr sidecar so the engine can invoke it during execution and replay.

- `AddDaprWorkflowVersioning` layers the versioning extension on top, which is what makes `IsPatched` and multiple named workflow types work. `AddDaprWorkflowVersioning` also automatically registers the workflow types in the application.

## Apply a Version Patch for Small, Additive Changes

Use a patch when the change is additive, existing steps keep executing in the same order, and you want one workflow type to serve both old and new instances. The pattern is a `context.IsPatched("FeatureName")` guard. Instances started after the deployment follow the path where `IsPatched` is `true`. In-flight instances replay through the `else` branch, so every decision point still matches what the engine recorded.

1. In the EnterpriseDiagnostics demo application open the `DiagnosticsWorkflow.cs` file located in `EnterpriseDiagnostics\EnterpriseDiagnostics.ApiService\Workflows\`.
2. Add the following code to the `DiagnosticsWorkflow` underneath the `AnalyzeSecuritySystemsActivity` and remove the existing `var recommendationsInput = ...` code block:

  ```csharp
  RecommendationsInput recommendationsInput;
  if (context.IsPatched("AddWeaponsAnalysis"))
  {
      var weaponsResult = await context.CallActivityAsync<AnalysisResult>(
          nameof(AnalyzeWeaponSystemsActivity),
          new AnalysisInput(input.ShipName, input.DiagnosticsDate, input.EngineerName, "Weapon Systems"));

      recommendationsInput = new RecommendationsInput(
          input.ShipName,
          input.DiagnosticsDate,
          input.EngineerName,
          hullResult,
          warpCoreResult,
          securityResult,
          weaponsResult);
  }
  else
  {
      recommendationsInput = new RecommendationsInput(
          input.ShipName,
          input.DiagnosticsDate,
          input.EngineerName,
          hullResult,
          warpCoreResult,
          securityResult);
  }
  ```

  Workflow instances scheduled before the patch follow the `else` branch during replay and finish with their original three-analysis recommendations. New workflow instances pick up the weapons analysis activity.

3. Add the registration of the `AnalyzeWeaponSystemsActivity` to the other activity registration in the Program.cs file:

  ```csharp
  options.RegisterActivity<AnalyzeWeaponSystemsActivity>();
  ```

## Verify the Patch Behaviour

1. Restart the application using `aspire run`.
2. Resume the previously paused workflow (`diag-001`) by making this curl request:

  ```shell
  curl -X POST http://localhost:5467/resume/diag-001
  ```

  This workflow instance should now continue without calling the `AnalyzeWeaponSystemsActivity`.
3. Start a new workflow instance by calling the `/start` endpoint:

  ```shell
  curl -X POST http://localhost:5467/start \
    -H "Content-Type: application/json" \
    -d '{
      "id": "diag-001-patch",
      "shipName": "USS Enterprise NCC-1701-D",
      "diagnosticsDate": "2370-04-08",
      "engineerName": "Geordi La Forge"
    }'
  ```

  The `diag-001-patch` workflow instance should continue calling all four activities.

4. Start a second workflow instance of the patched workflow (using ID `diag-001-patch-2`)and pause it so it can be resumed later when another bigger change is be introduced. Use the following curl command to pause the workflow instance:

  ```shell
  curl -X POST http://localhost:5467/pause/diag-001
  ```

  The workflow should have the `suspended` status now.

5. Stop the Aspire solution using again `CTRL+C` in the terminal where Aspire is running.

## Use a Named Version for Larger Changes

You can introduce multiple patches in a workflow, you can even nest patches, but patching has its limits and the workflow definition can become cluttered. Once you have many patches or introduce a large workflow change (e.g. going from task chaining to fan-out/fan-in) use a new named workflow type and keep the old workflow, so existing instances can still run to completion.

The EnterpriseDiagnostics demo contains additional workflow definitions alongside the original `DiagnosticsWorkflow` in the `EnterpriseDiagnostics\EnterpriseDiagnostics.ApiService\Workflows` folder. 

1. Rename the `DiagnosticsWorkflowV2.cs.temp` to `DiagnosticsWorkflowV2.cs`
2. Inspect the `DiagnosticsWorkflowV2` code. This V2 version of the workflow uses the fan-out/fan-in pattern for the analysis activities. This is a large structural change compared to the original version, so a named version makes more sense here:

  ```csharp
  // Define activity tasks to run the four analyses in parallel
  var hullTask = context.CallActivityAsync<AnalysisResult>(
      nameof(AnalyzeHullActivity),
      new AnalysisInput(input.ShipName, input.DiagnosticsDate, input.EngineerName, "Hull"));

  var warpCoreTask = context.CallActivityAsync<AnalysisResult>(
      nameof(AnalyzeWarpCoreActivity),
      new AnalysisInput(input.ShipName, input.DiagnosticsDate, input.EngineerName, "Warp Core"));

  var securityTask = context.CallActivityAsync<AnalysisResult>(
      nameof(AnalyzeSecuritySystemsActivity),
      new AnalysisInput(input.ShipName, input.DiagnosticsDate, input.EngineerName, "Security Protocols"));

  var weaponsTask = context.CallActivityAsync<AnalysisResult>(
      nameof(AnalyzeWeaponSystemsActivity),
      new AnalysisInput(input.ShipName, input.DiagnosticsDate, input.EngineerName, "Weapon Systems"));

  // Fan-out/fan-in: wait for all analyses to complete
  await Task.WhenAll(hullTask, warpCoreTask, securityTask, weaponsTask);
  ```

Both workflow types stay registered at the same time, no changes required in the `Program.cs` file. Existing instances keep replaying against `DiagnosticsWorkflow`. New instances are scheduled against V2. Note that the workflow name in the `/start` endpoint in `Program.cs` does not need to be changed to V2, the `AddDaprWorkflowVersioning` has built-in logic to figure out there is a new version of that same workflow.

## Verify the Named Version Behaviour

1. Restart the application using `aspire run`.
2. Resume the previously paused workflow (`diag-001-patch-2`) by making this curl request:

  ```shell
  curl -X POST http://localhost:5467/resume/diag-001-patch-2
  ```

  The `diag-001-patch-2` workflow instance should now continue and call all four analysis activities in sequence.
3. Start a new workflow instance by calling the `/start` endpoint:

  ```shell
  curl -X POST http://localhost:5467/start \
    -H "Content-Type: application/json" \
    -d '{
      "id": "diag-002",
      "shipName": "USS Enterprise NCC-1701-D",
      "diagnosticsDate": "2370-04-08",
      "engineerName": "Geordi La Forge"
    }'
  ```

  The `diag-002` workflow instance should use fan-out/fan-in instead of task chaining for the analysis activities.

4. Stop the Aspire solution using again `CTRL+C` in the terminal where Aspire is running.

## Run with Catalyst

Catalyst is an enterprise platform that provides durability and security when running workflows, AI agents & MCP servers. Catalyst has a built-in workflow engine powered by Dapr. Catalyst is platform for production workloads, with many features to manage and inspect Dapr Workflow and agentic AI applications.

You can connect your local application to Catalyst for debugging purposes and getting a better understanding of the workflow execution. Let's update the `AppHost.cs` and configure the Aspire solution to use Catalyst instead of Dapr locally.

### Prerequisites

- [Catalyst account](https://catalyst.diagrid.io/)
- [Diagrid CLI](https://docs.diagrid.io/references/catalyst/catalyst-cli-intro)

### Update the Aspire solution

1. Add the Aspire-Catalyst integration by installing this Nuget package:

   ```shell
   dotnet add EnterpriseDiagnostics.AppHost/EnterpriseDiagnostics.AppHost.csproj package Diagrid.Aspire.Hosting.Catalyst
   ```

2. Remove the Valkey integration:

  ```shell
  dotnet remove EnterpriseDiagnostics.AppHost/EnterpriseDiagnostics.AppHost.csproj package Aspire.Hosting.Valkey
  ```

3. Remove the Dapr integration:

  ```shell
  dotnet remove EnterpriseDiagnostics.AppHost/EnterpriseDiagnostics.AppHost.csproj package CommunityToolkit.Aspire.Hosting.Dapr
  ```

4. Replace the complete `AppHost.cs` code with the following:

  ```csharp
  using Diagrid.Aspire.Hosting.Catalyst;

  var builder = DistributedApplication.CreateBuilder(args);

  // This configures a new project in Catalyst with a managed state store for workflow state.
  var catalystProject = builder.AddCatalystProject("wf-aspire", new()
      {
          EnableManagedWorkflow = true,
      });
      

  // The apiService will not use a Dapr sidecar anymore but will use the Catalyst.
  var workflowApp = builder.AddProject<Projects.EnterpriseDiagnostics_ApiService>("wf-app")
      .WithCatalyst(catalystProject);

  builder.Build().Run();
  ```

5. Restart the application using `aspire run`.
  On the first usage of starting the solution with Catalyst some Catalyst resources are created which can take a couple of minutes.
6. Once all the Aspire resources are up and running make a new POST request to the `/start` endpoint to start a new workflow execution:

```shell
  curl -X POST http://localhost:5467/start \
    -H "Content-Type: application/json" \
    -d '{
      "id": "diag-002-catalyst",
      "shipName": "USS Enterprise NCC-1701-D",
      "diagnosticsDate": "2370-04-08",
      "engineerName": "Geordi La Forge"
    }'
  ```

1. Now use the Catalyst web UI and navigate to the [workflow page](https://catalyst.r1.diagrid.io/workflows/names) via _Operate -> Workflows_.
2. Select the DiagnosticsWorkflow in the list and inspect the workflow info on the detail page. Notice that there is a dropdown for the version information next to the workflow name.
3. You can drill down into the individual workflow executions by selecting an _Instance ID_ in the _Executions_ table. There you can use the workflow graph to inspect workflow executions, activity inputs and outputs, and durations.

## Summary

You now have two techniques for evolving Dapr workflows without breaking in-flight instances. Version patches with `context.IsPatched` let you ship small, additive changes while existing histories replay cleanly. Named workflow versions such as `DiagnosticsWorkflowV2` let you make structural changes by running old and new types side by side. Both rely on `AddDaprWorkflowVersioning`, and both are demonstrated in the EnterpriseDiagnostics demo.

Eager to learn more? Have a look at our [upcoming webinars](https://www.diagrid.io/webinars). If you're new to Dapr or Dapr Workflow, try the free lessons at [Dapr University](https://www.diagrid.io/dapr-university).

If you have any questions about Dapr Workflow please join the [Dapr Discord](https://bit.ly/dapr-discord) and look for the _#workflow_ channel.

## Resources

- [Dapr Workflow versioning docs](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-versioning/)
- [Build Dapr Applications Faster with Aspire and Diagrid Catalyst](https://www.diagrid.io/blog/build-dapr-applications-faster-aspire-catalyst)
- [Improving the Local Dapr Workflow Experience with the Diagrid Dashboard](https://www.diagrid.io/blog/improving-the-local-dapr-workflow-experience-diagrid-dashboard)