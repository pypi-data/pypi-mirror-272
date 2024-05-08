'''
# replace this

# Documentation API

[API](API.md)
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.pipelines as _aws_cdk_pipelines_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="cdk-vpc-toumoro-projen.IVpcBase")
class IVpcBase(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="maxAzs")
    def max_azs(self) -> typing.Optional[jsii.Number]:
        ...

    @builtins.property
    @jsii.member(jsii_name="natGateways")
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        ...


class _IVpcBaseProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-vpc-toumoro-projen.IVpcBase"

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @builtins.property
    @jsii.member(jsii_name="maxAzs")
    def max_azs(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAzs"))

    @builtins.property
    @jsii.member(jsii_name="natGateways")
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "natGateways"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IVpcBase).__jsii_proxy_class__ = lambda : _IVpcBaseProxy


class PipelineCdk(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-vpc-toumoro-projen.PipelineCdk",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        pipeline_name: builtins.str,
        repo_branch: builtins.str,
        repo_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param pipeline_name: 
        :param repo_branch: 
        :param repo_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceedf17f538e1a011af99657f624fdd1cdcad9d2ce3df10fc34579cbd0624176)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PipelineProps(
            pipeline_name=pipeline_name, repo_branch=repo_branch, repo_name=repo_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> _aws_cdk_pipelines_ceddda9d.CodePipeline:
        return typing.cast(_aws_cdk_pipelines_ceddda9d.CodePipeline, jsii.get(self, "pipeline"))


@jsii.data_type(
    jsii_type="cdk-vpc-toumoro-projen.PipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "pipeline_name": "pipelineName",
        "repo_branch": "repoBranch",
        "repo_name": "repoName",
    },
)
class PipelineProps:
    def __init__(
        self,
        *,
        pipeline_name: builtins.str,
        repo_branch: builtins.str,
        repo_name: builtins.str,
    ) -> None:
        '''
        :param pipeline_name: 
        :param repo_branch: 
        :param repo_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50cf7eb99d3d759662423d61e0ed40c985556393d9616cafef73823a224c239)
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument repo_branch", value=repo_branch, expected_type=type_hints["repo_branch"])
            check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pipeline_name": pipeline_name,
            "repo_branch": repo_branch,
            "repo_name": repo_name,
        }

    @builtins.property
    def pipeline_name(self) -> builtins.str:
        result = self._values.get("pipeline_name")
        assert result is not None, "Required property 'pipeline_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_branch(self) -> builtins.str:
        result = self._values.get("repo_branch")
        assert result is not None, "Required property 'repo_branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_name(self) -> builtins.str:
        result = self._values.get("repo_name")
        assert result is not None, "Required property 'repo_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpcBase(
    _aws_cdk_aws_ec2_ceddda9d.Vpc,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-vpc-toumoro-projen.VpcBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: IVpcBase,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3010ee1a172e4b1e59ff3f52ffda9e2c13c33133ed35298483e4ecbad5cb08)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.Vpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Vpc, jsii.get(self, "vpc"))


__all__ = [
    "IVpcBase",
    "PipelineCdk",
    "PipelineProps",
    "VpcBase",
]

publication.publish()

def _typecheckingstub__ceedf17f538e1a011af99657f624fdd1cdcad9d2ce3df10fc34579cbd0624176(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    pipeline_name: builtins.str,
    repo_branch: builtins.str,
    repo_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50cf7eb99d3d759662423d61e0ed40c985556393d9616cafef73823a224c239(
    *,
    pipeline_name: builtins.str,
    repo_branch: builtins.str,
    repo_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3010ee1a172e4b1e59ff3f52ffda9e2c13c33133ed35298483e4ecbad5cb08(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IVpcBase,
) -> None:
    """Type checking stubs"""
    pass
