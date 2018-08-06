import React from 'react';
import {Grid, Form} from 'semantic-ui-react';
import VitalRecordForm from "./vitalRecordForm";

class BirthSearchForm extends React.Component {
    constructor() {
        super()
        this.state = {
            gender: '',
            fatherName: '',
            motherName: '',
            birthPlace: '',
            lastName: '',
            firstName: '',
            middleName: '',
        }
    }

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Group>
                            <Form.Input label="First Name"
                                        name="firstName"
                                        placeholder="First Name"
                                        onChange={(e, {value}) => {
                                            this.setState({firstName: value})
                                            this.props.callBack("firstName", value, this.props.index, this.props.state.firstName)
                                        }}
                                        value={this.state.firstName}
                            />
                            <Form.Input label="Middle Name"
                                        name="middleName"
                                        placeholder="Middle Name"
                                        onChange={(e, {value}) => {
                                            this.setState({middleName: value})
                                            this.props.callBack("middleName", value, this.props.index, this.props.state.middleName)
                                        }}
                                        value={this.state.middleName}
                            />
                            <Form.Input label="Last Name"
                                        name="lastName"
                                        placeholder="Last Name"
                                        onChange={(e, {value}) => {
                                            this.setState({lastName: value})
                                            this.props.callBack("lastName", value, this.props.index, this.props.state.lastName)
                                        }}
                                        value={this.state.lastName}
                            />
                        </Form.Group>
                        <Form.Input label="Birth Place"
                                    name="birthPlace"
                                    placeholder="BirthPlace"
                                    onChange={(e, {value}) => {
                                        this.setState({birthPlace: value})
                                        this.props.callBack("birthPlace", value, this.props.index, this.props.state.birthPlace)
                                    }}
                                    value={this.state.birthPlace}
                        />
                        <Form.Select label="Gender"
                                     required
                                     name="gender"
                                     placeholder="Gender"
                                     options={this.props.genderOptions}
                                     onChange={(e, {value}) => {
                                         this.setState({gender: value});
                                         this.props.callBack("gender", value, this.props.index, this.props.state.gender);
                                     }}
                                     value={this.state.value}
                        />
                        <Form.Input label="Mother Name"
                                    name="motherName"
                                    placeholder="Mother Name"
                                    onChange={(e, {value}) => {
                                        this.setState({motherName: value})
                                        this.props.callBack("motherName", value, this.props.index, this.props.state.motherName)
                                    }}
                                    value={this.state.motherName}
                        />
                        <Form.Input label="Father Name"
                                    name="fatherName"
                                    placeholder="Father Name"
                                    onChange={(e, {value}) => {
                                        this.setState({fatherName: value})
                                        this.props.callBack("fatherName", value, this.props.index, this.props.state.fatherName)
                                    }}
                                    value={this.state.fatherName}
                        />
                        <VitalRecordForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} boroughOptions={this.props.boroughOptions}/>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

class BirthCertForm extends React.Component {
    constructor() {
        super()
        this.state = {
            gender: '',
            fatherName: '',
            motherName: '',
            birthPlace: '',
            lastName: '',
            firstName: '',
            middleName: '',
            certificateNum: '',

        }
    }

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column>
                        <Form.Input label="Certificate Number"
                                    name="certificateNum"
                                    placeholder="Certificate Number"
                                    onChange={(e, {value}) => {
                                        this.setState({certificateNum: value})
                                        this.props.callBack("certificateNum", value, this.props.index, this.props.state.certificateNum)
                                    }}
                                    value={this.state.certificateNum}
                        />
                        <BirthSearchForm callBack={this.props.callBack} index={this.props.index}
                                         state={this.props.state} boroughOptions={this.props.boroughOptions}
                                         genderOptions={this.props.genderOptions}/>
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export {BirthSearchForm, BirthCertForm};