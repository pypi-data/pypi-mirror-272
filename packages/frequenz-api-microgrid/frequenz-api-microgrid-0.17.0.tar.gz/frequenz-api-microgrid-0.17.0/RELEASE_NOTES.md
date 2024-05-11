# Frequenz Microgrid API Release Notes

## Summary

In this release, the Microgrid API has been updated to use the latest version
of `frequenz-api-common`, in addition a few improvements and a bug fix.

## Upgrading

- This release upgrades `frequenz-api-common` to version `v0.6.1`. Please refer
  to the release notes for [v0.6.0](https://github.com/frequenz-floss/frequenz-api-common/releases/tag/v0.6.0)
  and [v0.6.1](https://github.com/frequenz-floss/frequenz-api-common/releases/tag/v0.6.1)
  of `frequenz-api-common` for more information.

- A new RPC named `AddComponentBounds` has been introduced, which accepts only
  inclusive bounds. The old RPCs `AddComponentInclusionBounds` and
  `AddComponentExclusionBounds` have been removed.

- The enum `ComponentBoundsTargetMetric` has been removed in favour of the
  `Metric` enum from `frequenz-api-common`.

- The polarity of reactive power has been changed to follow the IEEE 1459-2010
  standard definitions. In this standard, positive reactive power is inductive
  (current is lagging the voltage), and negative reactive power is capacitive
  (current is leading the voltage).

## New Features

- The `AddComponentBoundsRequest` message has a field `validity_duration` which
  allows the user to specify the duration for which the bounds are valid. The
  bounds will be automatically removed after the specified duration. The client
  can select between 5 seconds, 1 minute, 5 minutes, and 15 minutes. If set to
  `UNSPECIFIED`, the bounds will be valid for a default duration of 5 seconds.

- The request messages `SetComponentPowerActiveRequest` and
  `SetComponentPowerReactiveRequest` have a new field named `request_lifetime`
  which allows the user to specify the duration for which the power setpoints
  are valid. If this field is not specified in a request, the power setpoint
  will be valid for 60 seconds.

## Bug Fixes

- The CI was unable to catch unused imports in the proto file before. This has
  been fixed by adding a new step to the CI to build using `protoc` with the
  `--fatal-warnings` flag.
